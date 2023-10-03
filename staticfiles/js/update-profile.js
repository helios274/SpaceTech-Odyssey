const profilePicture = document.getElementById("profilePicture");
const profilePictureInput = document.getElementById("id_profile_photo");

profilePictureInput.addEventListener("change", function () {
  const selectedImage = profilePictureInput.files[0];
  if (selectedImage) {
    const reader = new FileReader();
    reader.onload = function (event) {
      profilePicture.src = event.target.result;
    };
    reader.readAsDataURL(selectedImage);
  }
});
