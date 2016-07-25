(function() {
  if (!window.postMessage) return;

  if (window === window.parent) return;

  var currentHeight;

  function publishHeight() {
    var height = document.body.offsetHeight;
    if (currentHeight === height) return;
    currentHeight = height;

    window.parent.postMessage({height: currentHeight}, "*");
  }

  function autoPublish() {
    publishHeight();
    setTimeout(function() {
      autoPublish();
    }, 500);
  }

  autoPublish();

  window.addEventListener('load', function() {
    publishHeight();
  }, false);
})();

