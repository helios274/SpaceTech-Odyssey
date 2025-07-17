$(document).ready(function () {
  const commentSection = $("#comment-section");
  const postId = commentSection.data("post-id");
  const staticProfileImageURL = commentSection.data("static-profile-url");
  const arrowIconSrc = commentSection.data("arrow-icon-src");
  const isUserAuthenticated =
    commentSection.data("is-authenticated") === "True" ? true : false;
  const userId = commentSection.data("current-user-id");
  var messageId = 0;
  var commentOffset = 0;
  var commentLimit = 5;
  var replyOffset = 0;
  var replyLimit = 5;

  const arrowIcon = `
  <span class="arrow">
  <img src="${arrowIconSrc}" class="h-5 w-5" alt="show hide replies icon"/>
  </span>
`;

  function timeElapsed(date) {
    const now = new Date();
    const past = new Date(date);
    const diff = now - past;

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const weeks = Math.floor(days / 7);
    const months = Math.floor(days / 30);
    const years = Math.floor(days / 365);

    if (seconds < 60) {
      return seconds === 1 ? "1 second ago" : `${seconds} seconds ago`;
    } else if (minutes < 60) {
      return minutes === 1 ? "1 minute ago" : `${minutes} minutes ago`;
    } else if (hours < 24) {
      return hours === 1 ? "1 hour ago" : `${hours} hours ago`;
    } else if (days < 7) {
      return days === 1 ? "1 day ago" : `${days} days ago`;
    } else if (weeks < 5) {
      return weeks === 1 ? "1 week ago" : `${weeks} weeks ago`;
    } else if (months < 12) {
      return months === 1 ? "1 month ago" : `${months} months ago`;
    } else {
      return years === 1 ? "1 year ago" : `${years} years ago`;
    }
  }

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

  function commentActionButtons(comment) {
    return `
    ${
      isUserAuthenticated
        ? `
        ${
          userId === comment.user_id
            ? `
            <button type="button" class="edit-comment" data-comment-id="${comment.id}">Edit</button>
            <button type="button" class="delete-comment" data-comment-id="${comment.id}">Delete</button>
          `
            : ""
        }
        ${
          !comment.parent
            ? `
            <button type="button" class="reply" data-comment-id="${comment.id}" id="comment-${comment.id}">Reply</button>
            `
            : ""
        }
        `
        : ""
    }
    ${
      comment?.replies_count > 0
        ? `
          <button type="button" class="show-replies" data-comment-id="${comment.id}" data-offset="0" data-limit="5">
            ${arrowIcon}
            Show replies
          </button>`
        : ""
    }
  `;
  }

  function userProfileElement(comment) {
    return `
    <a href="/profile/${comment.user_id}">
      <img src="${
        comment.user_profile_photo
          ? comment.user_profile_photo
          : staticProfileImageURL
      }" alt="Profile Image" class="w-12 h-11 xl:w-12 xl:h-12 rounded-full">
    </a>
  `;
  }

  function userDataElement(comment) {
    return `
    <p class="text-sm">
      ${
        userId === comment.user_id
          ? `<strong>You</strong>`
          : `<strong>${comment.user}</strong>`
      }
      <span class="font-light">&emsp;${timeElapsed(comment.created_at)}</span>
    </p>
  `;
  }

  function commentCard(comment) {
    return `
    <div class="mb-7 flex flex-col" id="comment-${comment.id}">
      <div class="flex space-x-4">
          ${userProfileElement(comment)}
          <div class="flex flex-col w-full">
              ${userDataElement(comment)}
              ${
                !comment.parent
                  ? `
                <p class="comment-content mt-2 text-sm sm:text-base" id="comment-${comment.id}" data-comment-id="${comment.id}">
                  ${comment.content}
                </p>
                `
                  : `
                <p class="comment-content mt-2 text-sm sm:text-base">
                  ${comment.content}
                </p>
                `
              }
        
              <div class="flex space-x-3 mt-2 text-sm">
                  ${commentActionButtons(comment)}
              </div>
              ${
                !comment.parent
                  ? `
                  <div class="reply-form-container mt-4 hidden flex-col"></div>
                  <div class="replies-container mt-4 hidden flex-col"></div>
                  `
                  : ""
              }               
          </div>
      </div>
  </div>  
`;
  }

  // load comments handler
  function loadComments(offset, limit) {
    $.ajax({
      url: `/posts/${postId}/comments/`,
      method: "GET",
      data: {
        offset: offset,
        limit: limit,
      },
      success: function (data) {
        if (data.length < limit) {
          $("#load-more-comments").hide();
        }
        data.forEach(function (comment) {
          $("#comments").append(commentCard(comment));
        });
      },
      error: function (xhr, status, error) {
        showToastMessage("An error occurred while fetching comments", "error");
      },
      complete: function (xhr, status) {
        $("#load-more-comments img").fadeOut();
      },
    });
  }

  // load more comments handler
  $("#load-more-comments").click(function () {
    $(this).children("img").fadeIn();
    commentOffset += commentLimit;
    loadComments(commentOffset, commentLimit);
  });

  // add a comment handler
  $("#spinner-container").hide();
  $("#add-comment-form").on("submit", function (event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $("#spinner-container").fadeIn();
    $.ajax({
      url: `/posts/${postId}/comments/add/`,
      method: "POST",
      data: formData,
      success: function (comment) {
        $("#comments").prepend(commentCard(comment));
      },
      error: function (xhr, status, error) {
        showToastMessage("An error occurred while adding the comment", "error");
      },
      complete: function (xhr, status) {
        $("#id_content").val("");
        $("#spinner-container").fadeOut();
      },
    });
  });

  // reply form
  $("#comments").on("click", ".reply", function () {
    var commentId = $(this).data("comment-id");
    var replyForm = `
        <form class="reply-form" data-parent-id="${commentId}">
            <textarea class="content-textarea" name="content" rows="1" placeholder="Write a reply..."></textarea>
            <div class="flex space-x-2">
              <button type="button" class="cancel-reply" data-parent-id="${commentId}">Cancel</button>
              <button type="submit" class="save-reply">Reply</button>
            </div>
        </form>
    `;
    $(`#comment-${commentId} .reply-form-container`).prepend(replyForm);
    $(`#comment-${commentId} .reply-form-container`).slideDown(300);
    $(this).hide();
  });

  // cancel reply form
  $(document).on("click", ".cancel-reply", function () {
    var commentId = $(this).data("parent-id");
    var replyButton = $(`[data-comment-id="${commentId}"]`).filter(function () {
      return $(this).text() === "Reply";
    });
    replyButton.fadeIn(300);
    $(`#comment-${commentId} .reply-form`).slideUp(300, function () {
      $(this).parent().hide();
      $(this).remove();
    });
  });

  function showRepliesBtnToggler(button) {
    if (button.text().includes("Show replies"))
      button.text("Hide replies").prepend(arrowIcon);
    else button.text("Show replies").prepend(arrowIcon);
    button.toggleClass("showing");
  }

  // show replies
  $("#comments").on("click", ".show-replies", function () {
    var commentId = $(this).data("comment-id");
    var repliesContainer = $(`#comment-${commentId} .replies-container`);
    const showRepliesBtn = $(this);
    const isEmpty = repliesContainer.is(":empty");
    replyOffset = 0;
    replyLimit = 5;
    if (isEmpty) {
      repliesContainer.hide();
      $.ajax({
        url: `/comments/${commentId}/replies/`,
        method: "GET",
        data: {
          offset: replyOffset,
          limit: replyLimit,
        },
        success: function (data) {
          data.forEach(function (reply) {
            repliesContainer.append(commentCard(reply));
          });
          if (data.length >= replyLimit) {
            repliesContainer.append(
              `
              <button id="load-more-replies-${commentId}" data-comment-id="${commentId}" class="w-full load-more-replies">
                Show More replies
              </button>
              `
            );
          }
          repliesContainer.slideDown();
          showRepliesBtnToggler(showRepliesBtn);
        },
        error: function (xhr, status, error) {
          showToastMessage(
            "An error occurred while loading the replies",
            "error"
          );
        },
      });
    } else {
      repliesContainer.slideToggle();
      showRepliesBtnToggler(showRepliesBtn);
    }
  });

  // load more replies handler
  $("#comments").on("click", ".load-more-replies", function () {
    var commentId = $(this).data("comment-id");
    var repliesContainer = $(`#comment-${commentId} .replies-container`);
    replyOffset += replyLimit;
    $.ajax({
      url: `/comments/${commentId}/replies/`,
      method: "GET",
      data: {
        offset: replyOffset,
        limit: replyLimit,
      },
      success: function (data) {
        if (data.length < replyLimit) {
          $(`#load-more-replies-${commentId}`).hide();
        }
        data.forEach(function (reply) {
          repliesContainer.append(commentCard(reply));
        });
      },
      error: function (xhr, status, error) {
        showToastMessage(
          "An error occurred while loading the replies",
          "error"
        );
      },
    });
  });

  // reply to a comment
  $("#comments").on("submit", ".reply-form", function (e) {
    e.preventDefault();
    var parentId = $(this).data("parent-id");
    var formData = $(this).serialize() + "&parent=" + parentId;
    const isEmpty = $(`#comment-${parentId} .replies-container`).is(":empty");
    var replyButton = $(`button[data-comment-id="${parentId}"]`).filter(
      function () {
        return $(this).text() === "Reply";
      }
    );
    $.post(`/posts/${postId}/comments/add/`, formData, function (data) {
      $(`#comment-${parentId} .replies-container`).prepend(commentCard(data));
      $(`#comment-${parentId} .reply-form`)
        .parent()
        .slideUp(function () {
          $(`#comment-${parentId} .reply-form`).remove();
        });
      replyButton.show();
      if (isEmpty) {
        replyButton.after(`
          <button type="button" class="show-replies" data-comment-id="${parentId}" data-offset="0" data-limit="5">
              ${arrowIcon}
              Show replies
            </button>
        `);
      }
    }).fail(function (xhr, status, error) {
      showToastMessage("An error occurred while replying to comment", "error");
    });
  });

  // edit comment handler
  $("#comments").on("click", ".edit-comment", function () {
    var commentId = $(this).data("comment-id");
    var commentContent = $(this).parent().siblings(".comment-content");
    commentContent.attr("contenteditable", "true");
    commentContent.focus();
    $(this).after(
      `<a href="#" class="save-comment" data-comment-id="${commentId}">Save</a>`
    );
    $(this).after(
      `<button type="button" class="cancel-save" data-comment-id="${commentId}">cancel</button>`
    );
    $(this).hide();
    $(this).siblings(".delete-comment").hide();
    $(this).siblings(".reply").hide();
  });

  // cancel save comment handler
  $("#comments").on("click", ".cancel-save", function () {
    var commentContent = $(this).parent().siblings(".comment-content");
    commentContent.attr("contenteditable", "false");
    $(this).siblings(".edit-comment").show();
    $(this).siblings(".delete-comment").show();
    $(this).siblings(".reply").show();
    $(this).siblings(".save-comment").remove();
    $(this).remove();
  });

  // save edited comment or reply handler
  $("#comments").on("click", ".save-comment", function (event) {
    event.preventDefault();
    var commentId = $(this).data("comment-id");
    var commentContent = $(this).parent().siblings(".comment-content").text();
    $.post(
      `/comments/${commentId}/edit/`,
      {
        content: commentContent,
      },
      function (data) {
        $(`#comment-${commentId} .comment-content`).attr(
          "contenteditable",
          "false"
        );
        $(`.cancel-save[data-comment-id="${commentId}"]`).remove();
        $(`.save-comment[data-comment-id="${commentId}"]`).remove();
        $(`.edit-comment[data-comment-id="${commentId}"]`).show();
        $(`.delete-comment[data-comment-id="${commentId}"]`).show();
        $(`.reply[data-comment-id="${commentId}"]`).show();
        showToastMessage("Saved successfully", "success");
      }
    ).fail(function (xhr, status, error) {
      showToastMessage("An error occurred while saving", "error");
    });
  });

  $("#comments").on("click", ".delete-comment", function (event) {
    event.preventDefault();
    var commentId = $(this).data("comment-id");
    if (confirm("Are you sure you want to delete this comment?")) {
      $.post(`/comments/${commentId}/delete/`, function (data) {
        $(`#comment-${commentId}`).remove();
        showToastMessage("Deleted successfully", "success");
      }).fail(function (xhr, status, error) {
        showToastMessage("An error occurred while deleting", "error");
      });
    }
  });

  // Initial load
  loadComments(commentOffset, commentLimit);

  // increase rows of textarea
  $("#comment-section").on("input", "textarea", function () {
    var textarea = $(this);
    var lines = textarea.val().split("\n").length;
    var newRows = Math.min(Math.max(lines, 2), 8);
    textarea.attr("rows", newRows);
  });
});
