jQuery(function () {
  $("#id_bio").parent().addClass("sm:col-span-2");
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
});
