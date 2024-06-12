window.addEventListener("DOMContentLoaded", function () {
    const tagsEl = /** @type {HTMLMetaElement} */ document.querySelector("meta[name=tags]");
    const bannerImage = document.querySelector("#banner-image");
    const tags = tagsEl ? tagsEl.getAttribute("content").split(",").map(s => s.trim()) : [];

    var name;
    if (Math.random() < 0.05) name = "chicken";
    else if (tags.includes("robotics")) name = "armdroid";
    else if (tags.includes("game-design")) name = "gaming";
    else if (tags.includes("electronics")) name = "soldering";
    else if (tags.includes("reverse-engineering")) name = "microscope";
    else {
        const a = ["lounging", "lounging", "working", ""];
        name = a[Math.floor(a.length * Math.random())];
        if (!name) return; // Don't change it from default
    }
    bannerImage.src = `/images/yazani/yazani_${name}_extracted.png`;
});
