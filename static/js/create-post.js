$(document).ready(function () {
  // function getCookie(name) {
  //   let cookieValue = null;
  //   if (document.cookie && document.cookie !== "") {
  //     const cookies = document.cookie.split(";");
  //     for (let i = 0; i < cookies.length; i++) {
  //       const cookie = cookies[i].trim();
  //       // Does this cookie string begin with the name we want?
  //       if (cookie.substring(0, name.length + 1) === name + "=") {
  //         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
  //         break;
  //       }
  //     }
  //   }
  //   return cookieValue;
  // }

  // const csrftoken = getCookie("csrftoken");

  // function csrfSafeMethod(method) {
  //   // these HTTP methods do not require CSRF protection
  //   return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  // }

  // $.ajaxSetup({
  //   beforeSend: function (xhr, settings) {
  //     if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //       xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //     }
  //   },
  // });

  // Model configuration
  var $modal = $("#modal");

  $("#openModal").on("click", function () {
    $modal.removeClass("hidden modal-close").addClass("flex modal-open");
  });

  $("#closeModal").on("click", function () {
    $modal.removeClass("modal-open").addClass("modal-close");
    setTimeout(function () {
      $modal.addClass("hidden");
    }, 300);
  });

  $(document).on("click", function (e) {
    if ($(e.target).is($modal) && !$modal.hasClass("hidden")) {
      $modal.removeClass("modal-open").addClass("modal-close");
      setTimeout(function () {
        $modal.addClass("hidden");
      }, 300);
    }
  });

  // Search or create tags configuration

  let selectedTags = [];

  $("#tag-search").on("input", function () {
    const query = $(this).val();
    if (query.length > 1) {
      $.ajax({
        url: "tags/search-tags",
        data: { query: query },
        success: function (data) {
          $("#tag-suggestions").empty().show();
          if (data.length > 0) {
            data.forEach(function (tag) {
              $("#tag-suggestions").append(
                `<div class="tag-suggestion" data-id="${tag.id}" data-name="${tag.name}">${tag.name}</div>`
              );
            });
          } else {
            $("#tag-suggestions").append(
              '<div class="tag-suggestion" data-id="new" data-name="' +
                query +
                '">Create new tag: ' +
                query +
                "</div>"
            );
          }
        },
      });
    } else {
      $("#tag-suggestions").empty().hide();
    }
  });

  $(document).on("click", ".tag-suggestion", function () {
    const tagId = $(this).data("id");
    const tagName = $(this).data("name");
    if (tagId === "new") {
      $.ajax({
        url: "tags/add-tag",
        method: "POST",
        data: {
          name: tagName,
          // csrfmiddlewaretoken: csrftoken,
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader(
            "X-CSRFToken",
            $('input[name="csrfmiddlewaretoken"]').val()
          );
        },
        success: function (data) {
          selectedTags.push(data.name);
          $("#selected-tags").append(
            `<div class="tag">${data.name}<span class="remove-tag" data-name="${data.name}">&times;</span></div>`
          );
          updateTagsInput();
        },
      });
    } else {
      selectedTags.push(tagName);
      $("#selected-tags").append(
        `<div class="tag">${tagName}<span class="remove-tag" data-name="${tagName}">&times;</span></div>`
      );
      updateTagsInput();
    }
    $("#tag-search").val("");
    $("#tag-suggestions").empty().hide();
  });

  $(document).on("click", ".remove-tag", function () {
    const tagName = $(this).data("name");
    selectedTags = selectedTags.filter((tag) => tag !== tagName);
    $(this).parent().remove();
    updateTagsInput();
  });

  function updateTagsInput() {
    $("#tags").val(selectedTags.join(","));
  }

  $(".submit-btn").on("click", function (e) {
    if (selectedTags.length === 0) {
      e.preventDefault();
    }
  });

  // Blog image upload to cloudinary
  $("#upload-image").click(function () {
    var fileInput = $(
      '<input type="file" accept="image/*" style="display: none;">'
    );
    fileInput.on("change", function (e) {
      var file = e.target.files[0];

      // Upload image to Django view using AJAX
      var formData = new FormData();
      formData.append("image", file);

      $.ajax({
        url: "/posts/create-post/upload/post_cover", // Use URL template tag
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function (xhr) {
          xhr.setRequestHeader(
            "X-CSRFToken",
            $('input[name="csrfmiddlewaretoken"]').val()
          );
        },
        success: function (response) {
          if (response.success) {
            var imageUrl = response.url;
            var contentTextarea = $("#id_content");
            var cursorPos = contentTextarea.prop("selectionStart");
            var content = contentTextarea.val();
            var newContent =
              content.substring(0, cursorPos) +
              `![image description](${imageUrl})${content.substring(
                cursorPos
              )}`;
            contentTextarea.val(newContent);
            contentTextarea.focus();
            $("#image_url").val(imageUrl);
          } else {
            console.error("Error uploading image:", response.error);
            // Handle upload errors (optional)
          }
        },
        error: function (err) {
          console.error("Error:", err);
          // Handle AJAX errors (optional)
        },
      });
    });
    fileInput.click();
  });
});
