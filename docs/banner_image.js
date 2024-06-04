(function () {
    const tagsEl = /** @type {HTMLMetaElement} */ document.querySelector("meta[name=tags]");
    if (!tagsEl) return;
    const bannerImage = document.querySelector("#banner-image");
    const tags = tagsEl.getAttribute("content").split(",").map(s => s.trim()).sort();

    var name;
    if (Math.random() < 0.05) name = "chicken";
    else if (tags.includes("robotics")) name = "armdroid";
    else if (tags.includes("game-design")) name = "gaming";
    else if (tags.includes("electronics")) name = "soldering"
    else if (tags.includes("reverse-engineering")) name = "microscope";
    else {
        const a = ["lounging", "lounging", "working", null];
        name = a[Math.floor(a.length * Math.random())];
        if (name == null) return; // Don't change it
    }
    bannerImage.src = `/images/yazani/yazani_${name}_extracted.png`;
})();
