window.ui = {
  state: 'loading',
  readyToCollect: false,
  nExamples: 0,
  nTrainings: 0,

  setContent: function (key, value) {
    $('[data-content="' + key + '"]').html(value);
  },

  showInfo: function (text, dontFlash) {
    this.setContent('info', text);
    if (!dontFlash) {
      $('#info').addClass('flash');
      new Audio('hint.mp3').play();
      setTimeout(function () {
        $('#info').removeClass('flash');
      }, 1000);
    }
  },

  onWebcamEnabled: function () {
    this.state = 'finding face';
    this.showInfo('Пожалуйста, посмотрите в камеру! ', true);
  },

  onFoundFace: function () {
    if (this.state == 'finding face') {
      this.state = 'collecting';
      this.readyToCollect = true;
      this.showInfo(
        '<h3>Давайте начинать!</h3>' +
          'Собирайте точки данных, перемещая мышь по экрану, следя за курсором глазами и несколько раз нажимая клавишу пробела',
        true
      );
    }
  },

  onAddExample: function (nTrain, nVal) {
    this.nExamples = nTrain + nVal;
    this.setContent('n-train', nTrain);
    this.setContent('n-val', nVal);
    if (nTrain >= 2) {
      $('#start-training').prop('disabled', false);
    }
    if (this.state == 'collecting' && this.nExamples == 5) {
      this.showInfo(
        '<h3>Так держать!</h3>' +
          'Продолжайте собирать и переподготовлять! Вы также можете нарисовать тепловую карту, которая покажет вам, где у вашей модели есть сильные и слабые стороны.'
      );
    }
    if (this.state == 'collecting' && this.nExamples == 25) {
      this.showInfo(
        '<h3>Отличная работа!</h3>' +
          'Теперь, когда у вас есть несколько примеров, давайте обучим нейронную сеть!<br> ' +
          'Нажмите кнопку обучения в правом верхнем углу!'
      );
    }
    if (this.state == 'trained' && this.nExamples == 50) {
      this.showInfo(
        '<h3>Отличная работа</h3>' +
          'Вы собрали много примеров. При желании можете попробовать снова!'
      );
    }
    if (nTrain > 0 && nVal > 0) {
      $('#store-data').prop('disabled', false);
    }
  },

  onFinishTraining: function () {
    this.nTrainings += 1;
    $('#target').css('opacity', '0.9');
    $('#draw-heatmap').prop('disabled', false);
    $('#reset-model').prop('disabled', false);
    $('#store-model').prop('disabled', false);

    if (this.nTrainings == 1) {
      this.state = 'trained';
      this.showInfo(
        '<h3>Текущих данных недостаточно</h3>' +
          'Цель должна начать следовать за вашими глазами.<br>' +
          'Соберите больше данных для обучения! Продолжайте следовать за курсором мыши и нажимать пробел.'
      );
    } else if (this.nTrainings == 2) {
      this.state = 'trained_twice';
      this.showInfo(
        '<h3>Становится лучше! </h3>' +
          'Продолжайте собирать и переобучать!<br>' +
          'Вы также можете нарисовать тепловую карту, которая покажет вам, где у вашей  ' +
          'модели есть сильные и слабые стороны.'
      );
    } else if (this.nTrainings == 3) {
      this.state = 'trained_thrice';
      this.showInfo(
        'Если ваша модель переобучена, помните, что вы можете сбросить ее в любое время '
      );
    } else if (this.nTrainings == 4) {
      this.state = 'trained_thrice';
      this.showInfo('<h3>Отличная работа!</h3>' + '');
    }
  },
};
