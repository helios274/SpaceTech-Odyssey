$(document).ready(function () {
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
});
