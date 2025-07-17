$(document).ready(function () {
  const profilePicture = $("#profilePicture");
  const profilePictureInput = $("#id_profile_photo");

  profilePictureInput.on("change", function () {
    const selectedImage = this.files[0];
    if (selectedImage) {
      const reader = new FileReader();
      reader.onload = function (event) {
        profilePicture.attr("src", event.target.result);
      };
      reader.readAsDataURL(selectedImage);
    }
  });
});
