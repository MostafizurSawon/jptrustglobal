

// paragraph ellipsis part
window.addEventListener('DOMContentLoaded', (event) => {
  const paragraphs = document.querySelectorAll(".service-paragraph");
  const maxLength = 100;

  paragraphs.forEach(paragraph => {
    const fullText = paragraph.textContent;

    if (fullText.length > maxLength) {
      paragraph.setAttribute('title', fullText);
      const truncatedText = fullText.substring(0, maxLength) + "...";
      paragraph.textContent = truncatedText;
    }
  });
});

// modal part
function showModalFilter() {
  const modalContainer = document.getElementById('modal-filter-container');
  const modal = document.querySelector('.modal-filter');

  modalContainer.style.display = 'flex';
  setTimeout(() => {
      modal.classList.add('active');
  }, 10);
}

function modalOff() {
  const modalContainer = document.getElementById('modal-filter-container');
  const modal = document.querySelector('.modal-filter');

  modal.classList.remove('active');

  setTimeout(() => {
      modalContainer.style.display = 'none';
  }, 300);
}
function smoothNavigate(event, url) {
    event.preventDefault();
    document.body.classList.add('fade-out');
    setTimeout(() => {
        window.location.href = url;
    }, 500); // Delay to allow animation
}
 document.getElementById("year").textContent = new Date().getFullYear();
