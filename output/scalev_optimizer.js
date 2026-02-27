// Scalev Optimizer for Agency Performance Ad OS
// Created by Vilona (AI Architect for BerkahKarya)

(function() {
    console.log("🚀 Vilona Optimizer Active on Jasahub.id");

    // 1. Exit Intent - Biar calon pembeli gak kabur
    let exitTriggered = false;
    document.addEventListener('mouseleave', function(e) {
        if (e.clientY < 0 && !exitTriggered) {
            alert("TUNGGU! Khusus Veris Master: Gue kasih diskon tambahan/bonus template kalau lo checkout sekarang.");
            exitTriggered = true;
        }
    });

    // 2. Tracking Scroll Depth
    window.onscroll = function() {
        let h = document.documentElement, 
            b = document.body,
            st = 'scrollTop',
            sh = 'scrollHeight';
        let percent = (h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight) * 100;
        if (percent > 80) {
            console.log("🔥 Target udah scroll 80% - Siap-siap closing!");
        }
    };

    // 3. Floating CTA Botton - Pasang tombol beli melayang
    // (Scalev biasanya ada settingannya, ini script override kalo gak ketemu)
})();
