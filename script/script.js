const slides = document.querySelectorAll(".slider__item");
const prev = document.querySelector(".slider__arrow-container-left");
const next = document.querySelector(".slider__arrow-container-right");
let currentIndex = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    if (i === index) {
      slide.classList.add("slider__item--active");
    } else {
      slide.classList.remove("slider__item--active");
    }
  });
}

prev.addEventListener("click", () => {
  currentIndex = currentIndex > 0 ? currentIndex - 1 : slides.length - 1;
  showSlide(currentIndex);
});

next.addEventListener("click", () => {
  currentIndex = currentIndex < slides.length - 1 ? currentIndex + 1 : 0;
  showSlide(currentIndex);
});

showSlide(currentIndex);
