/*globals window */
var portalBrasil = {
  init: function () {
    this.tileBannerRotativo();
    this.alturaBannerRotativo();
  },
  // Tile Banner Rotativo
  corrigeAlturaFaixa: function () {
    if ($(".template-compose #tile_banner_rotativo").length === 0) {
      var imgBannerRotativo    = $('#tile_banner_rotativo .activeSlide .banner img'),
        credito              = $('#tile_banner_rotativo .activeSlide .credito'),
        botoesBannerRotativo = $('#tile_banner_rotativo .button-nav');

      var sobrescrito = $('#tile_banner_rotativo').hasClass('chamada_sobrescrito');
      if (sobrescrito) {
        botoesBannerRotativo.css('top',
                                 imgBannerRotativo.height()         -
                                 botoesBannerRotativo.height()      +
                                 (credito ? credito.height() : 0)   -
                                 18);
      } else {
        botoesBannerRotativo.css('top',
                                 imgBannerRotativo.height()         -
                                 botoesBannerRotativo.height()      +
                                 (credito ? credito.height() : 0));
      }
    }
  },
  tileBannerRotativo: function () {
    if ($('#tile_banner_rotativo').length > 0) {
      $('#tile_banner_rotativo .button-nav, .orderTiles .button-nav').on('click focus mouseover', function (e) {
        e.preventDefault();
        $("#tile_banner_rotativo li").removeClass('activeSlide');
        $(this).closest('li').addClass('activeSlide');
        portalBrasil.corrigeAlturaFaixa();
      });

      var updateCarrossel = function () {
        if (($('#tile_banner_rotativo a:hover').length === 0)   &&
            ($('#tile_banner_rotativo a:focus').length === 0)   &&
            ($(".template-compose #tile_banner_rotativo").length === 0)) {

          var totalSlides = $("#tile_banner_rotativo li").length;

          if (totalSlides > 1) {
            var activeSlide       = $('#tile_banner_rotativo li.activeSlide'),
              activeSlideNumber = parseInt(activeSlide.attr('data-slidenumber'), 10),
              nextSlideNumber   = (activeSlideNumber % totalSlides) + 1,
              nextSlide         = $('#banner' + nextSlideNumber);

            activeSlide.removeClass('activeSlide');
            nextSlide.addClass('activeSlide');
            portalBrasil.corrigeAlturaFaixa();
          }
        }
        window.setTimeout(updateCarrossel, 4000);
      };
      window.setTimeout(updateCarrossel, 4000);
    }
  },
  resizeAlturaBannerRotativo: function () {
    if ($(".template-compose #tile_banner_rotativo").length === 0) {
      var containerBannerRotativo = $('#tile_banner_rotativo'),
        itemBannerRotativo = $('#tile_banner_rotativo li');

      var sobrescrito = $('#tile_banner_rotativo').hasClass('chamada_sobrescrito');

      // ajusta altura de cada item do banner
      var bannerMaior = 0;

      itemBannerRotativo.each(function () {
        var altura = ($(this).find('img')      ? $(this).find('img').height()      : 0)  +
                     ($(this).find('.credito') ? $(this).find('.credito').height() : 0)  +
                     ($(this).find('.title')   ? $(this).find('.title').height()   : 0)  +
                     ($(this).find('.descr')   ? $(this).find('.descr').height()   : 0);
        if (sobrescrito) {
          altura = altura - ($(this).find('.title')   ? $(this).find('.title').height()   : 0);
        }
        if (bannerMaior < altura) {
          bannerMaior = altura;
        }
      });
      itemBannerRotativo.css('height', bannerMaior);
      // ajusta altura do container do banner rotativo (22px = margin bottom default dos tiles)
      containerBannerRotativo.animate({'height': bannerMaior+10}, 100, portalBrasil.corrigeAlturaFaixa);
    }
  },
  alturaBannerRotativo: function () {
    $(window).resize(portalBrasil.resizeAlturaBannerRotativo);
  }
};

$(window).load(function () {
  if ($('#tile_banner_rotativo').length > 0) {
    portalBrasil.init();
    portalBrasil.resizeAlturaBannerRotativo();
  }
});
