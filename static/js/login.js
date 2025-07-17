jQuery(function () {
  $("#togglePassword").click(function () {
    const passwordField = $("#id_password");
    const passwordFieldType = passwordField.attr("type");
    $("#eye").toggleClass("hidden");
    $("#eye-off").toggleClass("hidden");
    if (passwordFieldType === "password") {
      passwordField.attr("type", "text");
    } else {
      passwordField.attr("type", "password");
    }
  });

  $("#login-form").on("submit", function () {
    $(".submit-btn").text("Loggin in...");
  });
});
