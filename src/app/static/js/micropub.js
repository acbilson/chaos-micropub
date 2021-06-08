document.addEventListener('readystatechange', function(event) {

  current_date = new Date().toISOString().split('.')[0]
  document.getElementById('log_date').setAttribute('value', current_date);
  document.getElementById('note_date').setAttribute('value', current_date);
});

// hides and shows forms based on post type
document.getElementById('post-type-log').addEventListener('click', function(event) {
  document.getElementById('log-form').style.display = '';
  document.getElementById('note-form').style.display = 'none';
});

document.getElementById('post-type-note').addEventListener('click', function(event) {
  document.getElementById('log-form').style.display = 'none';
  document.getElementById('note-form').style.display = '';
});
