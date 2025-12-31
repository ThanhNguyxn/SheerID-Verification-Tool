"""
SheerID Verification Tool - Core Verifier
All verification logic in one class
"""

import re
import time
from typing import Dict, Optional, Tuple

try:
    import httpx
except ImportError:
    print("Error: httpx required. Install: pip install httpx")
    exit(1)

from .config import PROGRAMS, SHEERID_API_URL, SHEERID_BASE_URL, VALID_START_STEPS, ERROR_TYPES
from .utils import (
    stats, generate_fingerprint, generate_name, generate_email, 
    generate_birth_date, random_delay, retry_with_backoff
)
from .universities import select_university, select_k12_school
from .generators import (
    generate_student_id, generate_teacher_certificate, 
    generate_teacher_badge, generate_enrollment_letter
)


class SheerIDVerifier:
    """
    Unified SheerID Verifier
    Supports: Student, Teacher, K12 Teacher
    """
    
    def __init__(self, verification_url: str, service_type: str = "spotify"):
        self.verification_url = verification_url
        self.service_type = service_type.lower()
        self.verification_id = self._parse_verification_id(verification_url)
        self.program = PROGRAMS.get(self.service_type)
        self.fingerprint = generate_fingerprint()
        self.client = httpx.Client(timeout=30.0)
        
        # Verification data
        self.first_name = None
        self.last_name = None
        self.email = None
        self.birth_date = None
        self.organization = None
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_verification_id(url: str) -> Optional[str]:
        """Extract verification ID from URL"""
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, url: str, body: Dict = None) -> Tuple[Dict, int]:
        """Make API request with retry"""
        headers = {"Content-Type": "application/json"}
        
        try:
            random_delay()  # Avoid rate limiting
            response = self.client.request(method=method, url=url, json=body, headers=headers)
            
            try:
                data = response.json()
            except:
                data = {"text": response.text}
            
            return data, response.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _upload_to_s3(self, upload_url: str, data: bytes, mime_type: str) -> bool:
        """Upload document to S3"""
        try:
            response = self.client.put(
                upload_url,
                content=data,
                headers={"Content-Type": mime_type},
                timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            print(f"      [ERROR] S3 upload failed: {e}")
            return False
    
    def check_link_state(self) -> Dict:
        """Check if verification link is valid"""
        if not self.verification_id:
            return {"valid": False, "error": "Invalid verification ID"}
        
        try:
            data, status = self._request(
                "GET",
                f"{SHEERID_API_URL}/verification/{self.verification_id}"
            )
            
            if status != 200:
                return {"valid": False, "error": f"HTTP {status}"}
            
            current_step = data.get("currentStep", "")
            
            if current_step in VALID_START_STEPS:
                return {"valid": True, "step": current_step}
            elif current_step == "success":
                return {"valid": False, "error": "Already verified"}
            elif current_step == "error":
                return {"valid": False, "error": "Verification error"}
            else:
                return {"valid": False, "error": f"Invalid step: {current_step}"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def verify(self) -> Dict:
        """Run verification based on service type"""
        if not self.verification_id:
            return {"success": False, "error": "Invalid verification URL"}
        
        if not self.program:
            return {"success": False, "error": f"Unknown service: {self.service_type}"}
        
        print(f"\n   Service: {self.program['name']}")
        print(f"   Type: {self.program['type']}")
        print(f"   Verification ID: {self.verification_id}")
        
        # Check link state first
        state = self.check_link_state()
        if not state.get("valid"):
            return {"success": False, "error": state.get("error")}
        
        print(f"   Link State: {state.get('step')}")
        
        # Route to appropriate verification method
        verify_type = self.program["type"]
        
        if verify_type == "student":
            return self._verify_student()
        elif verify_type == "teacher":
            return self._verify_teacher()
        elif verify_type == "k12_teacher":
            return self._verify_k12_teacher()
        else:
            return {"success": False, "error": f"Unknown type: {verify_type}"}
    
    def _verify_student(self) -> Dict:
        """Student verification flow"""
        try:
            # Generate student info
            self.first_name, self.last_name = generate_name()
            self.organization = select_university(prefer_usa=True, stats=stats)
            self.email = generate_email(self.first_name, self.last_name, self.organization.get("domain"))
            self.birth_date = generate_birth_date(min_age=18, max_age=25)
            
            print(f"\n   📚 Student: {self.first_name} {self.last_name}")
            print(f"   📧 Email: {self.email}")
            print(f"   🏫 School: {self.organization['name']}")
            print(f"   🎂 Birth Date: {self.birth_date}")
            
            # Step 1: Generate documents
            print("\n   → Step 1/3: Generating student ID...")
            doc_data = generate_student_id(self.first_name, self.last_name, self.organization["name"])
            print(f"      Document: {len(doc_data)/1024:.1f} KB")
            
            # Step 2: Submit personal info
            print("   → Step 2/3: Submitting student info...")
            body = {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "birthDate": self.birth_date,
                "email": self.email,
                "phoneNumber": "",
                "organization": {
                    "id": self.organization["id"],
                    "idExtended": self.organization["idExtended"],
                    "name": self.organization["name"]
                },
                "deviceFingerprintHash": self.fingerprint,
                "locale": "en-US",
                "metadata": {"marketConsentValue": True}
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_API_URL}/verification/{self.verification_id}/step/collectStudentPersonalInfo",
                body
            )
            
            if status != 200:
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Step 2 failed: {status}"}
            
            if isinstance(data, dict) and data.get("currentStep") == "error":
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Error: {data.get('errorIds', [])}"}
            
            current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
            print(f"      Current step: {current_step}")
            
            # Step 3: Upload document
            if current_step in ["docUpload", "pending"]:
                print("   → Step 3/3: Uploading document...")
                result = self._upload_document(doc_data, "student_id.png")
                if not result.get("success"):
                    stats.record_failure(self.organization["name"])
                    return result
            
            stats.record_success(self.organization["name"])
            print("\n   ✅ Verification submitted!")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "name": f"{self.first_name} {self.last_name}",
                "email": self.email,
                "school": self.organization["name"]
            }
            
        except Exception as e:
            if self.organization:
                stats.record_failure(self.organization["name"])
            return {"success": False, "error": str(e)}
    
    def _verify_teacher(self) -> Dict:
        """Teacher verification flow"""
        try:
            # Generate teacher info
            self.first_name, self.last_name = generate_name()
            self.organization = select_university(prefer_usa=True, stats=stats)
            self.email = generate_email(self.first_name, self.last_name, self.organization.get("domain"))
            self.birth_date = generate_birth_date(min_age=25, max_age=55)
            
            print(f"\n   👨‍🏫 Teacher: {self.first_name} {self.last_name}")
            print(f"   📧 Email: {self.email}")
            print(f"   🏫 School: {self.organization['name']}")
            print(f"   🎂 Birth Date: {self.birth_date}")
            
            # Step 1: Generate certificate
            print("\n   → Step 1/4: Generating teacher certificate...")
            doc_data = generate_teacher_certificate(self.first_name, self.last_name, self.organization["name"])
            print(f"      Document: {len(doc_data)/1024:.1f} KB")
            
            # Step 2: Submit personal info
            print("   → Step 2/4: Submitting teacher info...")
            body = {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "birthDate": self.birth_date,
                "email": self.email,
                "phoneNumber": "",
                "organization": {
                    "id": self.organization["id"],
                    "idExtended": self.organization["idExtended"],
                    "name": self.organization["name"]
                },
                "deviceFingerprintHash": self.fingerprint,
                "locale": "en-US",
                "metadata": {"marketConsentValue": True}
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_API_URL}/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                body
            )
            
            if status != 200:
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Step 2 failed: {status}"}
            
            if isinstance(data, dict) and data.get("currentStep") == "error":
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Error: {data.get('errorIds', [])}"}
            
            current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
            print(f"      Current step: {current_step}")
            
            # Step 3: Skip SSO if needed
            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                print("   → Step 3/4: Skipping SSO...")
                self._request("DELETE", f"{SHEERID_API_URL}/verification/{self.verification_id}/step/sso")
            
            # Step 4: Upload document
            print("   → Step 4/4: Uploading document...")
            result = self._upload_document(doc_data, "teacher_certificate.png")
            if not result.get("success"):
                stats.record_failure(self.organization["name"])
                return result
            
            stats.record_success(self.organization["name"])
            print("\n   ✅ Verification submitted!")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "name": f"{self.first_name} {self.last_name}",
                "email": self.email,
                "school": self.organization["name"]
            }
            
        except Exception as e:
            if self.organization:
                stats.record_failure(self.organization["name"])
            return {"success": False, "error": str(e)}
    
    def _verify_k12_teacher(self) -> Dict:
        """K12 Teacher (High School) verification flow"""
        try:
            # Generate K12 teacher info
            self.first_name, self.last_name = generate_name()
            self.organization = select_k12_school(stats=stats)
            self.email = generate_email(self.first_name, self.last_name)  # Generic email
            self.birth_date = generate_birth_date(min_age=25, max_age=55)
            
            print(f"\n   👩‍🏫 K12 Teacher: {self.first_name} {self.last_name}")
            print(f"   📧 Email: {self.email}")
            print(f"   🏫 School: {self.organization['name']}")
            print(f"   🎂 Birth Date: {self.birth_date}")
            
            # Step 1: Generate badge
            print("\n   → Step 1/4: Generating teacher badge...")
            doc_data = generate_teacher_badge(self.first_name, self.last_name, self.organization["name"])
            print(f"      Document: {len(doc_data)/1024:.1f} KB")
            
            # Step 2: Submit personal info
            print("   → Step 2/4: Submitting teacher info...")
            body = {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "birthDate": self.birth_date,
                "email": self.email,
                "phoneNumber": "",
                "organization": {
                    "id": self.organization["id"],
                    "idExtended": self.organization["idExtended"],
                    "name": self.organization["name"]
                },
                "deviceFingerprintHash": self.fingerprint,
                "locale": "en-US",
                "metadata": {"marketConsentValue": True}
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_API_URL}/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                body
            )
            
            if status != 200:
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Step 2 failed: {status}"}
            
            if isinstance(data, dict) and data.get("currentStep") == "error":
                stats.record_failure(self.organization["name"])
                return {"success": False, "error": f"Error: {data.get('errorIds', [])}"}
            
            current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
            print(f"      Current step: {current_step}")
            
            # Step 3: Skip SSO
            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                print("   → Step 3/4: Skipping SSO...")
                self._request("DELETE", f"{SHEERID_API_URL}/verification/{self.verification_id}/step/sso")
            
            # Step 4: Upload document
            print("   → Step 4/4: Uploading document...")
            result = self._upload_document(doc_data, "teacher_badge.png")
            if not result.get("success"):
                stats.record_failure(self.organization["name"])
                return result
            
            stats.record_success(self.organization["name"])
            print("\n   ✅ Verification submitted!")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "name": f"{self.first_name} {self.last_name}",
                "email": self.email,
                "school": self.organization["name"]
            }
            
        except Exception as e:
            if self.organization:
                stats.record_failure(self.organization["name"])
            return {"success": False, "error": str(e)}
    
    def _upload_document(self, doc_data: bytes, filename: str) -> Dict:
        """Request upload URL and upload document"""
        try:
            # Request upload URL
            body = {
                "files": [{
                    "fileName": filename,
                    "mimeType": "image/png",
                    "fileSize": len(doc_data)
                }]
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_API_URL}/verification/{self.verification_id}/step/docUpload",
                body
            )
            
            if status != 200:
                return {"success": False, "error": f"Upload request failed: {status}"}
            
            if not isinstance(data, dict) or not data.get("documents"):
                return {"success": False, "error": "No documents in response"}
            
            upload_url = data["documents"][0].get("uploadUrl")
            if not upload_url:
                return {"success": False, "error": "No upload URL"}
            
            # Upload to S3
            if not self._upload_to_s3(upload_url, doc_data, "image/png"):
                return {"success": False, "error": "S3 upload failed"}
            
            print("      Document uploaded successfully!")
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
