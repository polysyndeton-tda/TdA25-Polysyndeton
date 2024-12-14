<script>
  let organisationName = "";
  fetch("./api")
  .then(d => d.json())
  .then(d => {
    organisationName = d.organization;
  });
</script>

<main>
  <p>
  Hello TdA
  </p>
  <p>Another element</p>

  
  <h1>Organizace se jmenuje {organisationName}</h1>
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Similique, porro repellat dignissimos et corporis quibusdam veritatis quam qui provident ad. Totam quis quia eum libero temporibus dolores. Obcaecati, deleniti placeat?</p>
</main>
