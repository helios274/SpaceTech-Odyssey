jQuery(function () {
  var $messages = $("#messages");
  var $searchBtn = $("#search-btn");
  if ($messages.length) {
    setTimeout(function () {
      $messages.remove();
    }, 3990);
  }

  var $searchInput = $("#search-input");
  $searchInput.on("keyup", function () {
    if ($.trim($searchInput.val()) !== "") {
      $searchBtn.removeAttr("disabled");
    } else {
      $searchBtn.attr("disabled", true);
    }
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
