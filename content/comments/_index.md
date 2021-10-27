+++
Title = "Comments"
displayInMenu = false
+++
{{< raw >}}
<div class="remark42__last-comments" data-max="50"></div>
<script>

var remark_config = {
    host: "https://comments.alexbilson.dev", // hostname of remark server, same as REMARK_URL in backend config, e.g. "https://demo.remark42.com"
    site_id: 'remark42',
    components: ['last-comments']
  };

  (function(c) {
    for(var i = 0; i < c.length; i++){
      var d = document, s = d.createElement('script');
      s.src = remark_config.host + '/web/' + c[i] +'.js';
      s.defer = true;
      (d.head || d.body).appendChild(s);
    }
  })(remark_config.components);

</script>
{{< / raw >}}
