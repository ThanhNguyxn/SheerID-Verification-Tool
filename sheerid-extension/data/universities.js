/**
 * University data for SheerID verification
 * Extracted from spotify-verify-tool/main.py
 */

const UNIVERSITIES = [
  // =========== USA - HIGH PRIORITY (15 schools) ===========
  { id: 2565, name: "Pennsylvania State University-Main Campus", domain: "psu.edu", weight: 100 },
  { id: 3499, name: "University of California, Los Angeles", domain: "ucla.edu", weight: 98 },
  { id: 3491, name: "University of California, Berkeley", domain: "berkeley.edu", weight: 97 },
  { id: 1953, name: "Massachusetts Institute of Technology", domain: "mit.edu", weight: 95 },
  { id: 3113, name: "Stanford University", domain: "stanford.edu", weight: 95 },
  { id: 2285, name: "New York University", domain: "nyu.edu", weight: 96 },
  { id: 1426, name: "Harvard University", domain: "harvard.edu", weight: 92 },
  { id: 698, name: "Columbia University", domain: "columbia.edu", weight: 92 },
  { id: 3568, name: "University of Michigan", domain: "umich.edu", weight: 95 },
  { id: 3686, name: "University of Texas at Austin", domain: "utexas.edu", weight: 94 },
  { id: 378, name: "Arizona State University", domain: "asu.edu", weight: 93 },
  { id: 3521, name: "University of Florida", domain: "ufl.edu", weight: 91 },
  { id: 1217, name: "Georgia Institute of Technology", domain: "gatech.edu", weight: 90 },
  { id: 602, name: "Carnegie Mellon University", domain: "cmu.edu", weight: 89 },
  { id: 2506, name: "Ohio State University", domain: "osu.edu", weight: 88 },

  // =========== CANADA - SUPPORTED (5 schools) ===========
  { id: 328355, name: "University of Toronto", domain: "utoronto.ca", weight: 88 },
  { id: 4782066, name: "McGill University", domain: "mcgill.ca", weight: 85 },
  { id: 328315, name: "University of British Columbia", domain: "ubc.ca", weight: 86 },
  { id: 328317, name: "University of Waterloo", domain: "uwaterloo.ca", weight: 84 },
  { id: 328319, name: "University of Alberta", domain: "ualberta.ca", weight: 82 },

  // =========== UK - SUPPORTED (8 schools) ===========
  { id: 273409, name: "University of Oxford", domain: "ox.ac.uk", weight: 88 },
  { id: 273378, name: "University of Cambridge", domain: "cam.ac.uk", weight: 88 },
  { id: 273294, name: "Imperial College London", domain: "imperial.ac.uk", weight: 85 },
  { id: 273319, name: "University College London", domain: "ucl.ac.uk", weight: 84 },
  { id: 273381, name: "University of Edinburgh", domain: "ed.ac.uk", weight: 82 },
  { id: 273383, name: "University of Manchester", domain: "manchester.ac.uk", weight: 80 },
  { id: 273385, name: "King's College London", domain: "kcl.ac.uk", weight: 79 },
  { id: 273387, name: "London School of Economics", domain: "lse.ac.uk", weight: 81 },

  // =========== GERMANY - SUPPORTED (6 schools) ===========
  { id: 10011178, name: "Technical University of Munich", domain: "tum.de", weight: 85 },
  { id: 344450, name: "Ludwig Maximilian University of Munich", domain: "lmu.de", weight: 83 },
  { id: 344452, name: "Heidelberg University", domain: "uni-heidelberg.de", weight: 81 },
  { id: 344454, name: "Humboldt University of Berlin", domain: "hu-berlin.de", weight: 80 },
  { id: 344456, name: "RWTH Aachen University", domain: "rwth-aachen.de", weight: 82 },
  { id: 344458, name: "Free University of Berlin", domain: "fu-berlin.de", weight: 79 },

  // =========== FRANCE - SUPPORTED (5 schools) ===========
  { id: 329766, name: "Ecole Polytechnique", domain: "polytechnique.edu", weight: 82 },
  { id: 10148649, name: "PSL Research University", domain: "psl.eu", weight: 80 },
  { id: 329768, name: "Sorbonne University", domain: "sorbonne-universite.fr", weight: 81 },
  { id: 329770, name: "Sciences Po", domain: "sciencespo.fr", weight: 79 },
  { id: 329772, name: "HEC Paris", domain: "hec.edu", weight: 78 },

  // =========== AUSTRALIA - SUPPORTED (6 schools) ===========
  { id: 345301, name: "The University of Melbourne", domain: "unimelb.edu.au", weight: 85 },
  { id: 345303, name: "The University of Sydney", domain: "sydney.edu.au", weight: 83 },
  { id: 345276, name: "Australian National University", domain: "anu.edu.au", weight: 81 },
  { id: 345305, name: "University of Queensland", domain: "uq.edu.au", weight: 80 },
  { id: 345307, name: "Monash University", domain: "monash.edu", weight: 79 },
  { id: 345309, name: "UNSW Sydney", domain: "unsw.edu.au", weight: 82 },

  // =========== JAPAN - SUPPORTED (5 schools) ===========
  { id: 354085, name: "The University of Tokyo", domain: "u-tokyo.ac.jp", weight: 83 },
  { id: 353961, name: "Kyoto University", domain: "kyoto-u.ac.jp", weight: 81 },
  { id: 353963, name: "Osaka University", domain: "osaka-u.ac.jp", weight: 79 },
  { id: 353965, name: "Tohoku University", domain: "tohoku.ac.jp", weight: 78 },
  { id: 353967, name: "Tokyo Institute of Technology", domain: "titech.ac.jp", weight: 80 },

  // =========== BRAZIL - SUPPORTED (5 schools) ===========
  { id: 10042652, name: "University of Sao Paulo", domain: "usp.br", weight: 82 },
  { id: 10059316, name: "University of Campinas", domain: "unicamp.br", weight: 79 },
  { id: 412760, name: "Federal University of Rio de Janeiro", domain: "ufrj.br", weight: 78 },
  { id: 412762, name: "Federal University of Minas Gerais", domain: "ufmg.br", weight: 77 },
  { id: 412764, name: "Federal University of Rio Grande do Sul", domain: "ufrgs.br", weight: 76 },

  // =========== INDONESIA - SUPPORTED (5 schools) ===========
  { id: 10008577, name: "University of Indonesia", domain: "ui.ac.id", weight: 82 },
  { id: 10008584, name: "Institut Teknologi Bandung", domain: "itb.ac.id", weight: 80 },
  { id: 10008579, name: "Gadjah Mada University", domain: "ugm.ac.id", weight: 79 },
  { id: 10008581, name: "Airlangga University", domain: "unair.ac.id", weight: 77 },
  { id: 10008589, name: "Institut Teknologi Sepuluh Nopember", domain: "its.ac.id", weight: 78 },

  // =========== OTHER SUPPORTED COUNTRIES ===========
  // Singapore
  { id: 356355, name: "National University of Singapore", domain: "nus.edu.sg", weight: 85 },
  { id: 356356, name: "Nanyang Technological University", domain: "ntu.edu.sg", weight: 83 },
  // Netherlands
  { id: 345979, name: "Delft University of Technology", domain: "tudelft.nl", weight: 80 },
  { id: 345981, name: "University of Amsterdam", domain: "uva.nl", weight: 78 },
  // Mexico
  { id: 10019857, name: "Universidad Nacional Autónoma de México", domain: "unam.mx", weight: 80 },
  { id: 10019859, name: "Tecnológico de Monterrey", domain: "tec.mx", weight: 79 },
  // Hong Kong
  { id: 356575, name: "University of Hong Kong", domain: "hku.hk", weight: 82 },
  { id: 356577, name: "Chinese University of Hong Kong", domain: "cuhk.edu.hk", weight: 80 },
  // Turkey
  { id: 10012345, name: "Bogazici University", domain: "boun.edu.tr", weight: 78 },
  { id: 10012347, name: "Middle East Technical University", domain: "metu.edu.tr", weight: 77 },
];
