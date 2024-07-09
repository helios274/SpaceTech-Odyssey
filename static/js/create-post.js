$(document).ready(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

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
          csrfmiddlewaretoken: csrftoken,
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

  $("#id_sections-0-local_id").val(1);
  $("#id_text_blocks-0-local_section_id").val(1);
  $("#id_text_blocks-0-text").attr("required", true);

  // Add section
  $("#add-section").click(function () {
    var sectionFormIdx = $("#id_sections-TOTAL_FORMS").val();
    var sectionFormHtml = $("#section-form-template")
      .html()
      .replace(/__prefix__/g, sectionFormIdx);
    $("#formsetContainer").append(sectionFormHtml);
    $(`#id_sections-${sectionFormIdx}-local_id`).val(
      parseInt(sectionFormIdx) + 1
    );
    $("#id_sections-TOTAL_FORMS").val(parseInt(sectionFormIdx) + 1);
  });
  // remove section
  $(document).on("click", ".remove-section", function () {
    var sectionFormIdx = $("#id_sections-TOTAL_FORMS").val();
    $("#id_sections-TOTAL_FORMS").val(parseInt(sectionFormIdx) - 1);
    var sectionForm = $(this).closest(".section-form");
    var textBlockCount = sectionForm.find(".text-block-form").length;
    var textBlockFormIdx = $("#id_text_blocks-TOTAL_FORMS").val();
    $("#id_text_blocks-TOTAL_FORMS").val(
      parseInt(textBlockFormIdx) - textBlockCount
    );
    var imageBlockCount = sectionForm.find(".image-block-form").length;
    var imageBlockFormIdx = $("#id_image_blocks-TOTAL_FORMS").val();
    $("#id_image_blocks-TOTAL_FORMS").val(
      parseInt(imageBlockFormIdx) - imageBlockCount
    );
    var listBlockCount = sectionForm.find(".list-block-form").length;
    var listBlockFormIdx = $("#id_list_blocks-TOTAL_FORMS").val();
    $("#id_list_blocks-TOTAL_FORMS").val(
      parseInt(listBlockFormIdx) - listBlockCount
    );
    sectionForm.remove();
  });

  // Add text blocks
  $(document).on("click", ".add-text-block", function () {
    var textBlockFormIdx = $("#id_text_blocks-TOTAL_FORMS").val();
    var textBlockFormHtml = $("#text-block-form-template")
      .html()
      .replace(/__prefix__/g, textBlockFormIdx);
    $(this).siblings(".text-block-formset").append(textBlockFormHtml);
    var localSectionId = $(this).siblings().find('[name$="-local_id"]').val();
    $(`#id_text_blocks-${textBlockFormIdx}-local_section_id`).val(
      parseInt(localSectionId)
    );
    $(`#id_text_blocks-${textBlockFormIdx}-text`).attr("required", true);
    $("#id_text_blocks-TOTAL_FORMS").val(parseInt(textBlockFormIdx) + 1);
  });
  // remove text blocks
  $(document).on("click", ".remove-text-block", function () {
    $(this).closest(".text-block-form").remove();
    var textBlockFormIdx = $("#id_text_blocks-TOTAL_FORMS").val();
    $("#id_text_blocks-TOTAL_FORMS").val(parseInt(textBlockFormIdx) - 1);
  });

  // Add image blocks
  $(document).on("click", ".add-image-block", function () {
    var imageBlockFormIdx = $("#id_image_blocks-TOTAL_FORMS").val();
    var imageBlockFormHtml = $("#image-block-form-template")
      .html()
      .replace(/__prefix__/g, imageBlockFormIdx);
    $(this).siblings(".image-block-formset").append(imageBlockFormHtml);
    var localSectionId = $(this).siblings().find('[name$="-local_id"]').val();
    $(`#id_image_blocks-${imageBlockFormIdx}-local_section_id`).val(
      parseInt(localSectionId)
    );
    $(`#id_image_blocks-${imageBlockFormIdx}-image`).attr("required", true);
    $("#id_image_blocks-TOTAL_FORMS").val(parseInt(imageBlockFormIdx) + 1);
  });
  // remove image blocks
  $(document).on("click", ".remove-image-block", function () {
    $(this).closest(".image-block-form").remove();
    var imageBlockFormIdx = $("#id_image_blocks-TOTAL_FORMS").val();
    $("#id_image_blocks-TOTAL_FORMS").val(parseInt(imageBlockFormIdx) - 1);
  });

  // Add list blocks
  $(document).on("click", ".add-list-block", function () {
    var listBlockFormIdx = $("#id_list_blocks-TOTAL_FORMS").val();
    var listBlockFormHtml = $("#list-block-form-template")
      .html()
      .replace(/__prefix__/g, listBlockFormIdx);
    $(this).siblings(".list-block-formset").append(listBlockFormHtml);
    var localSectionId = $(this).siblings().find('[name$="-local_id"]').val();
    $(`#id_list_blocks-${listBlockFormIdx}-local_section_id`).val(
      parseInt(localSectionId)
    );
    $(`#id_list_blocks-${listBlockFormIdx}-items`).attr("required", true);
    $("#id_list_blocks-TOTAL_FORMS").val(parseInt(listBlockFormIdx) + 1);
  });
  // remove list blocks
  $(document).on("click", ".remove-list-block", function () {
    $(this).closest(".list-block-form").remove();
    var listBlockFormIdx = $("#id_list_blocks-TOTAL_FORMS").val();
    $("#id_list_blocks-TOTAL_FORMS").val(parseInt(listBlockFormIdx) - 1);
  });
});
