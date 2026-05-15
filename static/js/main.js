(function () {
    function initMobileMenu() {
        const toggle = document.querySelector("[data-menu-toggle]");
        const panel = document.querySelector("[data-menu-panel]");

        if (!toggle || !panel) {
            return;
        }

        toggle.addEventListener("click", function () {
            const isExpanded = toggle.getAttribute("aria-expanded") === "true";
            const nextState = !isExpanded;
            toggle.setAttribute("aria-expanded", String(nextState));
            panel.classList.toggle("is-open", nextState);
        });

        panel.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                toggle.setAttribute("aria-expanded", "false");
                panel.classList.remove("is-open");
            });
        });

        window.addEventListener("resize", function () {
            if (window.innerWidth >= 992) {
                toggle.setAttribute("aria-expanded", "false");
                panel.classList.remove("is-open");
            }
        });
    }

    function initSlideshow() {
        const slideshow = document.querySelector("[data-slideshow]");
        if (!slideshow) {
            return;
        }

        const slides = Array.from(slideshow.querySelectorAll(".slide"));
        if (!slides.length) {
            slideshow.setAttribute("data-missing", "true");
            return;
        }

        let missingCount = 0;

        slides.forEach(function (slide) {
            slide.addEventListener("error", function () {
                slide.dataset.missing = "true";
                missingCount += 1;
                if (missingCount >= slides.length) {
                    slideshow.setAttribute("data-missing", "true");
                }
            });
        });

        let currentIndex = 0;

        function nextSlide() {
            const visibleSlides = slides.filter(function (slide) {
                return slide.dataset.missing !== "true";
            });

            if (visibleSlides.length <= 1) {
                return;
            }

            slides[currentIndex].classList.remove("active");

            let attempts = 0;
            do {
                currentIndex = (currentIndex + 1) % slides.length;
                attempts += 1;
            } while (slides[currentIndex].dataset.missing === "true" && attempts <= slides.length);

            slides[currentIndex].classList.add("active");
        }

        if (slides.length > 1) {
            setInterval(nextSlide, 4800);
        }
    }

    function initScrollReveal() {
        const revealItems = document.querySelectorAll("[data-reveal]");
        if (!revealItems.length) {
            return;
        }

        if (!("IntersectionObserver" in window)) {
            revealItems.forEach(function (item) {
                item.classList.add("revealed");
            });
            return;
        }

        const observer = new IntersectionObserver(
            function (entries, obs) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("revealed");
                        obs.unobserve(entry.target);
                    }
                });
            },
            {
                rootMargin: "0px 0px -8% 0px",
                threshold: 0.2,
            }
        );

        revealItems.forEach(function (item) {
            observer.observe(item);
        });
    }

    function initFormEnhancements() {
        const form = document.querySelector(".start-plan-form");
        const submitButton = document.querySelector("[data-submit-btn]");

        if (!form || !submitButton) {
            return;
        }

        form.addEventListener("submit", function () {
            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";
        });
    }

    function initFooterBrandCrop() {
        const cropFrame = document.querySelector("[data-footer-brand-crop]");
        const brandImage = document.querySelector("[data-footer-brand-image]");

        if (!cropFrame || !brandImage) {
            return;
        }

        function applyCropRatio() {
            if (!brandImage.naturalWidth || !brandImage.naturalHeight) {
                return;
            }

            // Keep the center 50% of image height (crop top/bottom 25% each).
            const croppedRatio = brandImage.naturalWidth / (brandImage.naturalHeight * 0.5);
            cropFrame.style.aspectRatio = String(croppedRatio);
        }

        if (brandImage.complete) {
            applyCropRatio();
        }

        brandImage.addEventListener("load", applyCropRatio);
    }

    document.addEventListener("DOMContentLoaded", function () {
        initMobileMenu();
        initSlideshow();
        initScrollReveal();
        initFormEnhancements();
        initFooterBrandCrop();
    });
})();
