const exampleModal = document.getElementById('editCommentModal')
exampleModal.addEventListener('show.bs.modal', event => {
  const button = event.relatedTarget
  const recipient = button.getAttribute('data-bs-whatever')
  const modalBodyInput = exampleModal.querySelector('.modal-body input')
  modalBodyInput.value = recipient
})