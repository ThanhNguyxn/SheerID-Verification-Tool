// Fingerprint Spoofer - Inject vào MAIN world để bypass SheerID anti-fraud
// Spoof: Canvas, WebGL, Audio, Navigator, Screen

(function () {
    'use strict';

    // Random seed cho mỗi session
    const sessionSeed = Math.random().toString(36).substring(2, 15);

    // Simple hash function
    function simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    // Generate random but consistent values based on seed
    function seededRandom(seed) {
        const x = Math.sin(simpleHash(sessionSeed + seed)) * 10000;
        return x - Math.floor(x);
    }

    // ============ CANVAS FINGERPRINT SPOOF ============
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;

    // Thêm noise vào canvas data
    function addCanvasNoise(imageData) {
        const data = imageData.data;
        for (let i = 0; i < data.length; i += 4) {
            // Thêm noise nhỏ vào mỗi pixel
            const noise = Math.floor(seededRandom(i.toString()) * 3) - 1;
            data[i] = Math.max(0, Math.min(255, data[i] + noise));     // R
            data[i + 1] = Math.max(0, Math.min(255, data[i + 1] + noise)); // G
            data[i + 2] = Math.max(0, Math.min(255, data[i + 2] + noise)); // B
        }
        return imageData;
    }

    CanvasRenderingContext2D.prototype.getImageData = function (...args) {
        const imageData = originalGetImageData.apply(this, args);
        return addCanvasNoise(imageData);
    };

    HTMLCanvasElement.prototype.toDataURL = function (...args) {
        const ctx = this.getContext('2d');
        if (ctx) {
            try {
                const imageData = originalGetImageData.call(ctx, 0, 0, this.width, this.height);
                addCanvasNoise(imageData);
                ctx.putImageData(imageData, 0, 0);
            } catch (e) { }
        }
        return originalToDataURL.apply(this, args);
    };

    // ============ WEBGL FINGERPRINT SPOOF ============
    const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
    const originalGetExtension = WebGLRenderingContext.prototype.getExtension;

    const webglVendors = ['Google Inc.', 'Intel Inc.', 'NVIDIA Corporation', 'AMD'];
    const webglRenderers = [
        'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
        'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)',
        'ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)',
        'ANGLE (Intel, Intel(R) Iris(TM) Plus Graphics 640 Direct3D11 vs_5_0 ps_5_0)'
    ];

    const randomVendor = webglVendors[Math.floor(seededRandom('vendor') * webglVendors.length)];
    const randomRenderer = webglRenderers[Math.floor(seededRandom('renderer') * webglRenderers.length)];

    WebGLRenderingContext.prototype.getParameter = function (param) {
        const debugInfo = this.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
            if (param === debugInfo.UNMASKED_VENDOR_WEBGL) return randomVendor;
            if (param === debugInfo.UNMASKED_RENDERER_WEBGL) return randomRenderer;
        }
        return originalGetParameter.call(this, param);
    };

    // WebGL2 support
    if (typeof WebGL2RenderingContext !== 'undefined') {
        WebGL2RenderingContext.prototype.getParameter = WebGLRenderingContext.prototype.getParameter;
    }

    // ============ AUDIO FINGERPRINT SPOOF ============
    if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
        const OriginalAudioContext = window.AudioContext || window.webkitAudioContext;

        window.AudioContext = window.webkitAudioContext = function (...args) {
            const context = new OriginalAudioContext(...args);

            const originalCreateOscillator = context.createOscillator.bind(context);
            context.createOscillator = function () {
                const oscillator = originalCreateOscillator();
                // Thêm random nhỏ vào frequency
                const originalFrequency = oscillator.frequency;
                const noise = seededRandom('audio') * 0.0001;
                if (originalFrequency.value) {
                    originalFrequency.value += noise;
                }
                return oscillator;
            };

            return context;
        };
    }

    // ============ NAVIGATOR SPOOF ============
    const navigatorProps = {
        hardwareConcurrency: Math.floor(seededRandom('cores') * 8) + 2, // 2-10 cores
        deviceMemory: [2, 4, 8, 16][Math.floor(seededRandom('memory') * 4)],
        platform: ['Win32', 'MacIntel', 'Linux x86_64'][Math.floor(seededRandom('platform') * 3)]
    };

    Object.keys(navigatorProps).forEach(prop => {
        try {
            Object.defineProperty(navigator, prop, {
                get: () => navigatorProps[prop],
                configurable: true
            });
        } catch (e) { }
    });

    // Hide webdriver
    try {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            configurable: true
        });
    } catch (e) { }

    // ============ SCREEN SPOOF ============
    const screenResolutions = [
        { width: 1920, height: 1080 },
        { width: 1366, height: 768 },
        { width: 1536, height: 864 },
        { width: 1440, height: 900 },
        { width: 1280, height: 720 }
    ];
    const randomScreen = screenResolutions[Math.floor(seededRandom('screen') * screenResolutions.length)];

    try {
        Object.defineProperty(screen, 'width', { get: () => randomScreen.width, configurable: true });
        Object.defineProperty(screen, 'height', { get: () => randomScreen.height, configurable: true });
        Object.defineProperty(screen, 'availWidth', { get: () => randomScreen.width, configurable: true });
        Object.defineProperty(screen, 'availHeight', { get: () => randomScreen.height - 40, configurable: true });
        Object.defineProperty(screen, 'colorDepth', { get: () => 24, configurable: true });
        Object.defineProperty(screen, 'pixelDepth', { get: () => 24, configurable: true });
    } catch (e) { }

    // ============ TIMEZONE SPOOF ============
    const timezones = ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles'];
    const randomTZ = timezones[Math.floor(seededRandom('tz') * timezones.length)];

    const originalDateTimeFormat = Intl.DateTimeFormat;
    Intl.DateTimeFormat = function (...args) {
        if (args.length === 0 || (args.length === 1 && !args[0])) {
            args = [undefined, { timeZone: randomTZ }];
        }
        return new originalDateTimeFormat(...args);
    };
    Intl.DateTimeFormat.prototype = originalDateTimeFormat.prototype;

    console.log('[FingerprintSpoofer] Loaded - Session:', sessionSeed.substring(0, 6));
})();
