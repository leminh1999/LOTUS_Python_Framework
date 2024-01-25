let imageVisible = false; // Biến theo dõi trạng thái ẩn/hiện ảnh
let toggleCount = 0; // Biến đếm số lần nhấn nú

function toggleImage(imageId) {
  var imageContainer = document.getElementById(imageId);
  if (imageContainer.style.display === 'none') {
    imageContainer.style.display = 'block';
  } else {
    imageContainer.style.display = 'none';
  }
}

function toggleAllImages() {
  toggleCount++;
  imageVisible = toggleCount % 2 !== 0; // Đổi trạng thái ẩn/hiện ảnh dựa vào số lần nhấn chẵn/lẻ

  const imageContainers = document.querySelectorAll(".image-container");
  imageContainers.forEach((container) => {
    container.style.display = imageVisible ? "block" : "none";
  });
}

function showThumbnail(src, target) {
  const thumbnail = document.createElement("img");
  thumbnail.classList.add("thumbnail");
  thumbnail.src = src;
  document.body.appendChild(thumbnail);
}

function hideThumbnail() {
  const thumbnail = document.querySelector(".thumbnail");
  if (thumbnail) {
    thumbnail.remove();
  }
}