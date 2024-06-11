document.addEventListener("DOMContentLoaded", function() {
    var langSwitcher = document.createElement("select");
    langSwitcher.id = "lang-switcher";

    var languages = {
        'en': 'English',
        'ja': '日本語',
        'vi': 'Tiếng Việt'
    };

    for (var lang in languages) {
        var option = document.createElement("option");
        option.value = lang;
        option.text = languages[lang];
        langSwitcher.appendChild(option);
    }

    langSwitcher.addEventListener("change", function() {
        var selectedLang = this.value;
        var currentUrl = window.location.href;
        var newUrl = currentUrl.split('?')[0] + '?lang=' + selectedLang;
        window.location.href = newUrl;
    });

    document.getElementById("header").appendChild(langSwitcher);
});
