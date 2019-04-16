document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.nav-link').onclick = () => {
    document.querySelector('#recipe_title').innerHTML = 'Romantic Chicken Dinner for Two';
    document.querySelector('.list-unstyled').innerHTML = "";
    for (var i = 0; i < 5; i++) {
      li = document.createElement('li');
      li.innerHTML = "this is an idea"
      document.querySelector('.list-unstyled').appendChild(li);
    }
  }
  document.querySelector('#test').onclick = () => {
    const request = new XMLHttpRequest();
    request.open('POST', '/test');
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data.success) {
             alert("Success");
      document.querySelector('#recipe_title').innerHTML = data.name;
      document.querySelector('.list-unstyled').innerHTML = "";
      li = document.createElement('li');
      li.innerHTML = data.ing;
      document.querySelector('.list-unstyled').appendChild(li);
      p = document.createElement('p');
      p.innerHTML = data.steps;
      document.querySelector('#test2').appendChild(p);
    }
    else {
             alert("Error")
         }
    }

    const data = new FormData();
    // Send request
    request.send(data);
    return false;
  }
});
