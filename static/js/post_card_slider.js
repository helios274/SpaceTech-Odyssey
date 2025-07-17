jQuery(function () {
  const $carousel = $("#post-cards-container");
  const $buttons = $(".card-toggle-btn");
  const totalSlides = $carousel.children().length;
  let currentSlide = 0;
  let autoSlideInterval;

  // Function to move to a specific slide
  function moveToSlide(index) {
    $carousel.css("transform", `translateX(-${index * 100}%)`);
    currentSlide = index;
    updateActiveButton(index);
    resetAutoSlide();
  }

  // Update the active button's style
  function updateActiveButton(index) {
    $buttons.removeClass("card-toggle-btn-active"); // Remove active styles from all buttons
    $buttons.eq(index).addClass("card-toggle-btn-active"); // Add active styles to the current button
  }

  // Auto-slide function
  function autoSlide() {
    autoSlideInterval = setInterval(function () {
      let nextSlide = (currentSlide + 1) % totalSlides;
      moveToSlide(nextSlide);
    }, 3000); // 3-second delay
  }

  // Reset auto-slide interval
  function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlide();
  }

  // Button click event
  $buttons.on("click", function () {
    const index = $(this).data("card-num") - 1; // -1 to match 0-based index
    moveToSlide(index);
  });

  // Start the auto-slide
  autoSlide();

  // Initialize the first button as active
  updateActiveButton(currentSlide);
});
