$(document).ready(function () {
  var messageId = 0;

  // toast message handler
  function showToastMessage(messageString, type) {
    messageId += 1;
    const messageContainer = $("#messageContainer");
    if (messageContainer.length) {
      messageContainer.append(
        `
          <div class="message-body message-${
            type === "error" ? "danger" : "success"
          } message-enter" data-message-id="${messageId}">
            <p>${messageString}</p>
            <button type="button" class="message-close-btn" data-close-id="${messageId}">X</button>
          </div>
        `
      );
    } else {
      $("body").prepend(
        `
          <div id="messageContainer">
            <div class="message-body message-${
              type === "error" ? "danger" : "success"
            } message-enter" data-message-id="${messageId}">
              <p>${messageString}</p>
              <button type="button" class="message-close-btn" data-close-id="${messageId}">X</button>
            </div>
          </div>
        `
      );
    }
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
  }

  let selectedTags = [];

  $("#tag-search").on("input", function () {
    const query = $(this).val();
    if (query.length > 0) {
      $.ajax({
        url: "/posts/tags/search-tags",
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
        url: "/posts/tags/add-tag",
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

  // Blog image upload to cloudinary
  $("#upload-image").click(function () {
    const uploadLoader = $("#upload-loader");
    var fileInput = $(
      '<input type="file" accept="image/*" style="display: none;">'
    );
    fileInput.on("change", function (e) {
      var file = e.target.files[0];
      var formData = new FormData();
      formData.append("image", file);
      uploadLoader.fadeIn();

      $.ajax({
        url: "/posts/create-post/upload/post_cover",
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
            var scrollPos = contentTextarea.scrollTop();
            var content = contentTextarea.val();
            var markdownSyntax = `![image description](${imageUrl})`;
            var newContent =
              content.substring(0, cursorPos) +
              markdownSyntax +
              content.substring(cursorPos);

            contentTextarea.val(newContent);

            var newCursorPos = cursorPos + markdownSyntax.length;

            contentTextarea.focus();
            contentTextarea[0].setSelectionRange(newCursorPos, newCursorPos);

            contentTextarea.scrollTop(scrollPos);

            $("#image_url").val(imageUrl);
            showToastMessage("Image uploaded", "success");
          } else {
            showToastMessage("Error uploading image", "error");
          }
        },
        error: function (err) {
          showToastMessage("Error uploading image", "error");
        },
        complete: function (xhr, status) {
          uploadLoader.fadeOut();
        },
      });
    });
    fileInput.click();
  });

  // Modal handlers
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

  const submitLoader = '<div class="submit-loader ms-2"></div>';

  $("#post-form").on("submit", function () {
    $(".submit-btn").text("Updating").append(submitLoader);
  });
});
