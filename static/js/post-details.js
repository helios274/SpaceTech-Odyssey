$(document).ready(function () {
  // Like, dislike, and bookmark handlers
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  function updateIcons(status) {
    if (status.liked) {
      $("#likeOutlineIcon").addClass("hidden");
      $("#likeFilledIcon").removeClass("hidden");
    } else {
      $("#likeOutlineIcon").removeClass("hidden");
      $("#likeFilledIcon").addClass("hidden");
    }

    if (status.disliked) {
      $("#dislikeOutlineIcon").addClass("hidden");
      $("#dislikeFilledIcon").removeClass("hidden");
    } else {
      $("#dislikeOutlineIcon").removeClass("hidden");
      $("#dislikeFilledIcon").addClass("hidden");
    }

    if (status.bookmarked) {
      $("#bookmarkOutlineIcon").addClass("hidden");
      $("#bookmarkFilledIcon").removeClass("hidden");
    } else {
      $("#bookmarkOutlineIcon").removeClass("hidden");
      $("#bookmarkFilledIcon").addClass("hidden");
    }
  }

  function fetchPostStatus() {
    var slug = $("#like-button").data("slug");
    $.ajax({
      url: "/posts/" + slug + "/status/",
      method: "GET",
      success: function (response) {
        updateIcons(response);
      },
    });
  }

  if ($("#authStatus").val() === "True") {
    fetchPostStatus();

    $("#like-button").on("click", function () {
      var slug = $(this).data("slug");
      $.ajax({
        url: "/posts/" + slug + "/like/",
        method: "POST",
        success: function (response) {
          if (response.status === "liked") {
            $("#likeOutlineIcon").addClass("hidden");
            $("#likeFilledIcon").removeClass("hidden");
            $("#dislikeOutlineIcon").removeClass("hidden");
            $("#dislikeFilledIcon").addClass("hidden");
          } else {
            $("#likeOutlineIcon").removeClass("hidden");
            $("#likeFilledIcon").addClass("hidden");
            $("#dislikeOutlineIcon").removeClass("hidden");
            $("#dislikeFilledIcon").addClass("hidden");
          }
        },
      });
    });

    $("#dislike-button").on("click", function () {
      var slug = $(this).data("slug");
      $.ajax({
        url: "/posts/" + slug + "/dislike/",
        method: "POST",
        success: function (response) {
          if (response.status === "disliked") {
            $("#dislikeOutlineIcon").addClass("hidden");
            $("#dislikeFilledIcon").removeClass("hidden");
            $("#likeOutlineIcon").removeClass("hidden");
            $("#likeFilledIcon").addClass("hidden");
          } else {
            $("#likeOutlineIcon").removeClass("hidden");
            $("#likeFilledIcon").addClass("hidden");
            $("#dislikeOutlineIcon").removeClass("hidden");
            $("#dislikeFilledIcon").addClass("hidden");
          }
        },
      });
    });

    $("#bookmark-button").on("click", function () {
      var slug = $(this).data("slug");
      $.ajax({
        url: "/posts/" + slug + "/bookmark/",
        method: "POST",
        success: function (response) {
          if (response.status === "bookmarked") {
            $("#bookmarkOutlineIcon").addClass("hidden");
            $("#bookmarkFilledIcon").removeClass("hidden");
          } else {
            $("#bookmarkOutlineIcon").removeClass("hidden");
            $("#bookmarkFilledIcon").addClass("hidden");
          }
        },
      });
    });
  }

  // Modal
  function openModal() {
    $("#deleteModal").removeClass("hidden");
    setTimeout(() => $("#deleteModal .modal").addClass("modal-show"), 10); // Adding a slight delay for transition effect
  }

  function closeModal() {
    $("#deleteModal .modal").removeClass("modal-show");
    setTimeout(() => $("#deleteModal").addClass("hidden"), 300); // Match this duration with the CSS transition duration
  }

  // Show the modal when the delete button is clicked
  $("#deleteButton").click(function () {
    openModal();
  });

  // Close the modal when the cancel button is clicked
  $("#cancelButton").click(function () {
    closeModal();
  });

  // Close the modal when clicking outside the modal content
  $(document).click(function (event) {
    if (!$(event.target).closest(".sm\\:max-w-lg, #deleteButton").length) {
      closeModal();
    }
  });

  // Scroll button functionality
  const $scrollBtn = $("#scrollBtn");
  let isScrolledToBottom = false;

  $scrollBtn.on("click", function () {
    if (isScrolledToBottom) {
      // Scroll to the top
      $("html, body").animate({ scrollTop: 0 }, "fast");
    } else {
      // Scroll to the bottom
      $("html, body").animate(
        { scrollTop: $(document).height() - $(window).height() },
        "fast"
      );
    }
    isScrolledToBottom = !isScrolledToBottom;
  });

  $(window).on("scroll", function () {
    // Check if the user has scrolled to the bottom
    if ($(window).scrollTop() + $(window).height() === $(document).height()) {
      isScrolledToBottom = true;
      $("#arrowUpIcon").toggleClass("hidden");
      $("#arrowDownIcon").toggleClass("hidden");
    } else if ($(window).scrollTop() === 0) {
      isScrolledToBottom = false;
      $("#arrowUpIcon").toggleClass("hidden");
      $("#arrowDownIcon").toggleClass("hidden");
    }
  });

  $(".post-content p").has("img").addClass("flex justify-center");

  function moveElement() {
    var windowWidth = $(window).width();
    var $element = $("#postAuthorCard");

    if (windowWidth < 1280) {
      // Move to parent2 when the width is less than 768px
      if ($element.parent().attr("id") !== "parent1") {
        $("#parent1").append($element);
      }
    } else {
      // Move back to parent1 when the width is greater than or equal to 768px
      if ($element.parent().attr("id") !== "parent2") {
        $("#parent2").append($element);
      }
    }
  }

  // Run the function on initial load
  moveElement();

  // Run the function on window resize
  $(window).resize(function () {
    moveElement();
  });
});
