(function () {
  const save = (data, filename) => {
    const elem = document.createElement('a');
    elem.href = URL.createObjectURL(data);
    elem.download = filename;
    elem.click();
  };

  const download = (url, callback) => {
    fetch(url)
      .then(res => res.blob())
      .then(data => {
        callback(data);
      });
  }

  const downloadLink = document.querySelector('#download');
  if (downloadLink) {
    downloadLink.addEventListener('click', (evt) => {
      const fileName = downloadLink.dataset.file;
      console.log(fileName);
      download('/download/' + fileName, (data) => {
        save(data, fileName);
        location.href = '/removefile/' + fileName;
      });
    });
  }

  const downloadSample = (linkElemenet) => {
    const fileName = linkElemenet.dataset.file;
    console.log(fileName);
    download('/download/' + fileName, (data) => {
      save(data, fileName);
    });
  }

  const downloadLinkSeries = document.querySelector('#downloadseries');
  if (downloadLinkSeries) {
    downloadLinkSeries.addEventListener('click', (evt) => {
      downloadSample(downloadLinkSeries)
    });
  }
  const downloadLinkMovies = document.querySelector('#downloadmovies');
  if (downloadLinkMovies) {
    downloadLinkMovies.addEventListener('click', (evt) => {
      downloadSample(downloadLinkMovies)
    });
  }

  var date = new Date();
  document.querySelector('#date').innerHTML = date.getFullYear();
})();