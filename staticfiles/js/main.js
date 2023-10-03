jQuery(function () {
  var $messages = $("#messages");
  var $searchInput = $("#search-input");
  var $searchBtn = $("#search-btn");
  if ($messages.length) {
    setTimeout(function () {
      $messages.remove();
    }, 3990);
  }
  $searchInput.on("keyup", function () {
    if ($.trim($searchInput.val()) !== "") {
      $searchBtn.removeAttr("disabled");
    } else {
      $searchBtn.attr("disabled", true);
    }
  });
});
