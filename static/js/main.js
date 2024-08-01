jQuery(function () {
  // message functionality
  function showMessage(message) {
    message.addClass("message-enter-active");
  }

  function hideMessage(message) {
    message.addClass("message-exit-active");
    setTimeout(function () {
      message.remove();
    }, 300);
  }

  $("#messageContainer > div").each(function () {
    var message = $(this);
    setTimeout(function () {
      hideMessage(message);
    }, 3800);

    message.find("button").on("click", function () {
      hideMessage(message);
    });

    showMessage(message);
  });

  // Navbar dropdown toggle
  const $dropdownButton = $("#dropdownButton");
  const $dropdownMenu = $("#dropdownMenu");

  function closeDropdown() {
    if (!$dropdownMenu.hasClass("hidden")) {
      $dropdownMenu.removeClass("menu-open");
      setTimeout(() => $dropdownMenu.addClass("hidden"), 300);
    }
  }

  $dropdownButton.on("click", function (event) {
    event.stopPropagation();
    $dropdownMenu.toggleClass("hidden");
    if (!$dropdownMenu.hasClass("hidden")) {
      setTimeout(() => $dropdownMenu.addClass("menu-open"), 10);
    } else {
      closeDropdown();
    }
  });

  $(document).on("click", function (event) {
    if (!$(event.target).closest("#dropdownMenu, #dropdownButton").length) {
      closeDropdown();
    }
  });

  $(window).on("resize", function () {
    if (window.innerWidth >= 768) {
      closeDropdown();
    }
  });

  //Search bar
  $("#searchToggleBtn").on("click", function () {
    $("#searchBarContainer").toggleClass("md:flex");
  });

  // Carousel sliding
  let currentIndex = 0;
  const totalSlides = $("#carousel > div").length;
  let autoSlideInterval;
  function updateIndicators() {
    $(".indicator").removeClass("indicator-active");
    $(`.indicator[data-slide=${currentIndex}]`).addClass("indicator-active");
  }
  function moveToSlide(index) {
    $("#carousel").css("transform", `translateX(-${index * 100}%)`);
    currentIndex = index;
    updateIndicators();
  }
  function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    autoSlideInterval = setInterval(function () {
      let newIndex = currentIndex + 1;
      if (newIndex >= totalSlides) newIndex = 0;
      moveToSlide(newIndex);
    }, 3000);
  }
  $("#prev").click(function () {
    let newIndex = currentIndex - 1;
    if (newIndex < 0) newIndex = totalSlides - 1;
    moveToSlide(newIndex);
    resetAutoSlide();
  });
  $("#next").click(function () {
    let newIndex = currentIndex + 1;
    if (newIndex >= totalSlides) newIndex = 0;
    moveToSlide(newIndex);
    resetAutoSlide();
  });
  $(".indicator").click(function () {
    let index = $(this).data("slide");
    moveToSlide(index);
    resetAutoSlide();
  });
  resetAutoSlide();
  moveToSlide(0);
});
