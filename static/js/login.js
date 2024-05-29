jQuery(function () {
  var $password = $("#id_password");
  var $passwordToggler = $("#pwd-toggler");
  var $eyeIcon = $("#eye-icon");
  $password.addClass("flex-grow-1");
  $passwordToggler.on("click", function () {
    if ($password.attr("type") === "password") {
      $password.attr("type", "text");
      $eyeIcon.removeClass("bi-eye-slash-fill").addClass("bi-eye-fill");
    } else {
      $password.attr("type", "password");
      $eyeIcon.removeClass("bi-eye-fill").addClass("bi-eye-slash-fill");
    }
  });
});
