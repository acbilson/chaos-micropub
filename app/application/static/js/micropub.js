document.addEventListener('readystatechange', function(event) {

  current_date = new Date().toISOString().split('.')[0]
  document.getElementById('date').setAttribute('value', current_date);
});
