// script.js
document.addEventListener("DOMContentLoaded", function() {
    const articleList = document.getElementById("article-list");
    const articleModal = document.getElementById("article-modal");
    const articleContent = document.getElementById("article-content");
    const closeBtn = document.getElementsByClassName("close")[0];

    articleList.addEventListener("click", function(event) {
        if (event.target && event.target.matches(".headline")) {
            const articleItem = event.target.closest(".article-item");
            const articleData = articleItem.getAttribute("data-article");
            articleContent.innerHTML = articleData;
            articleModal.style.display = "block";
        }
    });

    closeBtn.addEventListener("click", function() {
        articleModal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target === articleModal) {
            articleModal.style.display = "none";
        }
    });
});
