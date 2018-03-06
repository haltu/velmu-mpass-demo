(function(window, angular, _, undefined) {

  var hmDesktop = angular.module('hmDesktop', []),
      // TODO: these need to be dynamic
      hmDesktopCardSize = {width: 190, height: 190};

  // index of helper cause IE8
  var indexOf = Array.prototype.indexOf ? function( ary, obj ) {
    return ary.indexOf( obj );
    } : function( ary, obj ) {
    for ( var i=0, len = ary.length; i < len; i++ ) {
      if ( ary[i] === obj ) {
        return i;
      }
    }
    return -1;
  };

  function removeFrom( obj, ary ) {
    var index = indexOf( ary, obj );
    if ( index !== -1 ) {
      ary.splice( index, 1 );
    }
  }

  hmDesktop.factory('hmCardActionService', ['$rootScope', 'hmHyperlinkService',
    function($rootScope, hmHyperlinkService) {

      var scope = $rootScope.$new();
      var $html = $('html');

      scope.actionHandlers = {};
      scope.handleCardAction = function handleCardAction(event, card) {

        var cardType = card.card_type || $rootScope.default_card_type;
        var handler = scope.actionHandlers[cardType];
        var isTouch = $html.hasClass('mod-touch-pointer');

        if (handler) {
          handler(card, isTouch, function stopEvent() {
            Hammer.utils.stopEvent(event);
          });
        }
        else if (isTouch && card.url) {
          Hammer.utils.stopEvent(event);
          hmHyperlinkService.open(card.url, '_blank');
        }

      };
      scope.registerHandler = function registerHandler(cardType, handler) {

        scope.actionHandlers[cardType] = handler;

      };

      return scope;

    }]);

  hmDesktop.factory('hmCardPreloadService', ['$rootScope', '$q', '$http', '$templateCache', 'hmCardStaticfilesService',
    function($rootScope, $q, $http, $templateCache, hmCardStaticfilesService) {

      var scope = $rootScope.$new();
      var headElement = document.getElementsByTagName('head')[0];

      scope.preloadCards = function preloadCards(cardList) {

        var deferreds = [];

        angular.forEach(cardList, function cardListIterator(card) {

          var cardType = card.card_type || $rootScope.default_card_type;
          var templateUrl = '/uiapi/1/dreamcards/cards/:card_type/get_template/'.replace(':card_type', cardType);
          var staticFilesDeferred = hmCardStaticfilesService.load(cardType);
          var templateDeferred = $http.get(templateUrl, {cache: $templateCache});
          deferreds.push(staticFilesDeferred, templateDeferred);

        });

        return $q.all(deferreds);

      };

      return scope;

    }]);

  hmDesktop.factory('hmCardStaticfilesService', ['$rootScope', '$q', '$http', '$templateCache',
    function($rootScope, $q, $http, $templateCache) {

      var scope = $rootScope.$new();
      var headElement = document.getElementsByTagName('head')[0];

      scope.loadedCardTypes = [];
      scope.load = function load(cardType) {

        var deferred = $q.defer();

        if (scope.loadedCardTypes.indexOf(cardType) != -1) {
          deferred.resolve();
          return deferred;
        }

        var staticfilesUrl = '/uiapi/1/dreamcards/cards/:card_type/get_resources/'.replace(':card_type', cardType);

        deferred = $http.get(staticfilesUrl, {cache: $templateCache})
        .success(function handleTemplateResponse(response) {

          var tempContainer = document.createElement('div');
          var newElement;
          var element;
          var tagName;
          var len;
          var i;

          tempContainer.insertAdjacentHTML('afterbegin', response);
          len = tempContainer.children.length;

          for (i = 0; i < len; i++) {
            element = tempContainer.children[i];
            tagName = element.tagName.toLowerCase();
            if (tagName == 'script') {
              newElement = document.createElement('script');
              newElement.setAttribute('src', element.getAttribute('src'));
              headElement.appendChild(newElement);
            }
            else if (tagName == 'link') {
              newElement = document.createElement('link');
              newElement.setAttribute('rel', 'stylesheet');
              newElement.setAttribute('href', element.getAttribute('href'));
              headElement.appendChild(newElement);
            }
          }

          scope.loadedCardTypes.push(cardType);

        })
        .error(function () {});

        return deferred;

      };

      return scope;

    }]);

  hmDesktop.directive('hmCard', ['$compile', '$http', '$templateCache', '$rootScope', 'hmCardStaticfilesService',
    function($compile, $http, $templateCache, $rootScope, hmCardStaticfilesService) {
      return {
        restrict: 'A',
        link: function linkingFn(scope, element, attrs) {

          var cardType = scope.card.card_type || $rootScope.default_card_type;
          var templateUrl = '/uiapi/1/dreamcards/cards/:card_type/get_template/'.replace(':card_type', cardType);

          scope.card.element = element;
          hmCardStaticfilesService.load(cardType);

          $http.get(templateUrl, {cache: $templateCache})
          .success(function handleTemplateResponse(response) {

            element.html(response).show();
            $compile(element.contents())(scope);
            scope.$emit('cardTemplateLoaded');

          })
          .error(function() {});

        }
      };
    }]);

  hmDesktop.controller('hmPackeryCtrl', ['$scope', '$element', '$attrs',
    function($scope, $element, $attrs) {
      $scope.$root.hmPackeryScope = $scope;
    }]);

  hmDesktop.directive('hmPackery', ['$parse', '$timeout', 'activePageService', 'hmAnimationService',
    function($parse, $timeout, activePageService, hmAnimationService) {
      return {
        restrict: 'A',
        controller: 'hmPackeryCtrl',
        compile: function compileFn(element, attrs) {
          element[0].insertAdjacentHTML('afterbegin', '<div class="grid-sizer"></div>');
          return {
            pre: function preLink(scope, element, attrs) {
              var relayoutTimeout, initTimeout;

              scope.itemsById = {};
              scope.pckry = new Packery(element[0], {
                itemSelector: '.hm-desktop-card',
                columnWidth: '.grid-sizer',
                rowHeight: '.grid-sizer',
                gutter: parseInt(element.find('.grid-sizer').css('margin-right')) || 10
              });
              element.data('packery', scope.pckry);
              element.css({opacity: ''});

              scope.pckry.on('layoutComplete', initAnimation);
              function initAnimation() {
                hmAnimationService.requestAnimation('page-enter');

                if(initTimeout) {
                  $timeout.cancel(initTimeout);
                }
                initTimeout = $timeout(function init() {
                  scope.pckry.off('layoutComplete', initAnimation);
                }, 100);
              }

              scope.pckry.on('dragItemPositioned', function(pckry, draggedItem) {
                var cardInstance = angular.element(draggedItem.element).scope().card;
                var idx = _.indexOf(scope.pckry.getItemElements(), draggedItem.element) + 1;
                activePageService.attachCard(cardInstance, idx);

                if(relayoutTimeout) {
                  $timeout.cancel(relayoutTimeout);
                }
                relayoutTimeout = $timeout(function reLayout() {
                  pckry.layout();
                });
              });

              activePageService.scope.$on('attach', handleAttach);
              activePageService.scope.$on('detach', handleDetach);

              function handleAttach(event, card, order, animate) {
                if(animate) {
                  hmAnimationService.requestAnimation('attach');
                }
              }

              function handleDetach(event, card, animate) {
                if(animate) {
                  hmAnimationService.requestAnimation('detach');
                }
              }

            }
          };
        }
      };
    }]);

  // Draggabilly overrides
  Draggabilly.prototype.setHandles = function() {
    this.handles = this.options.handle ?
    this.element.querySelectorAll( this.options.handle ) : [ this.element ];
  };

  Draggabilly.prototype.__dragEnd = Draggabilly.prototype.dragEnd;
  Draggabilly.prototype.dragEnd = function dragEnd(event, pointer) {
    if(this.isEnabled) {
      this.__dragEnd.call(this, event, pointer);
    }
  };

  Draggabilly.prototype.__dragMove = Draggabilly.prototype.dragMove;
  Draggabilly.prototype.dragMove = function dragMove(event, pointer) {
    if(this.isEnabled) {
      this.__dragMove.call(this, event, pointer);
    }
  };

  hmDesktop.directive('hmPackeryItem', ['$parse', '$timeout', 'hmCardActionService', 'activePageService', 'hmAnimationService',
    function($parse, $timeout, hmCardActionService, activePageService, hmAnimationService) {
      return {
        restrict: 'A',
        require: '^hmPackery',
        link: function linkingFn(scope, element, attrs) {
          var hammer, innerElement, draggie, items, item, startEvent,
              interactionDragTimeout, scrollableContainer, mainContent,
              removalBin, removalBinTop, removalBinBottom, removalBinParent,
              elementCornerPosition, removalBinPosition, removalBinDistance,
              isInteracting, isDragging, isMouseHold, isTouchDrag, isBinActive;

          element[0].cardScope = scope;
          removalBin = angular.element('.sidebar-button.bin');
          removalBinTop = removalBin.find('.fa').eq(0);
          removalBinBottom = removalBin.find('.fa').eq(1);
          removalBinParent = removalBin.parent();
          mainContent = angular.element('.main-content');
          scrollableContainer = element.closest('.scrollable');
          innerElement = undefined;
          items = scope.pckry.addItems(element[0]);
          scope.pckry.layoutItems(items, true);
          item = items[0];
          elementCornerPosition = {};
          removalBinPosition = {};

          draggie = new Draggabilly(element[0]);
          element.data('draggie', draggie);
          scope.pckry.bindDraggabillyEvents(draggie);

          if (!(hammer = element.data('hammer'))) {
            hammer = Hammer(element[0]);
            hammer.options.holdTimeout = 300;
            hammer.options.behavior.touchAction = 'pan-y';
            Hammer.utils.toggleBehavior(hammer.element, hammer.options.behavior, true);
            element.data('hammer', hammer);
          }

          // Store element by id for use in hmPackerySatellite
          scope.itemsById[scope.card.id] = {
            element: element,
            hammer: hammer,
            draggie: draggie,
            item: item,
            dragStart: handleDragStart,
            dragMove: handleDragMove,
            dragEnd: handleDragEnd
          };

          hammer.on('touch', handleTouch);
          hammer.on('tap', handleTap);
          hammer.on('dragstart hold', handleDragStart);
          hammer.on('drag', handleDragMove);
          hammer.on('dragend release', handleDragEnd);

          scope.$on('$destroy', function() {
            hammer.off('touch', handleTouch);
            hammer.off('tap', handleTap);
            hammer.off('dragstart hold', handleDragStart);
            hammer.off('drag', handleDragMove);
            hammer.off('dragend release', handleDragEnd);
          });

          scope.$on('cardTemplateLoaded', function() {
            innerElement = element.find('.card');
          });

          function handleTouch(event) {
            if(isInteracting || event.gesture.pointerType === 'mouse') {
              return;
            }
            isInteracting = true;
            interactionStart();

            if(isDragging) {
              Hammer.utils.stopEvent(event);
            }
          }

          function handleTap(event) {
            hmCardActionService.handleCardAction(event, scope.card);
          }

          function handleDragStart(event) {

            // We want to use the hold event for touch and drag event for mouse
            isMouseHold = event.type === 'hold' && event.gesture.pointerType == 'mouse';
            isTouchDrag = event.type === 'dragstart' && event.gesture.pointerType != 'mouse';
            if(isMouseHold || isTouchDrag) {
              if( ! isDragging) {
                interactionStop();
              }
              return;
            }

            if(event.gesture.pointerType != 'mouse' && ! isInteracting) {
              interactionStart();
            }

            isDragging = true;
            scrollableContainer.css({'-ms-scroll-limit': '0 0 0 0'});

            startEvent = event.gesture.startEvent.srcEvent;
            if (startEvent.type === 'touchstart') {
              draggie.dragStart(startEvent, startEvent.changedTouches[0]);
            } else {
              draggie.dragStart(startEvent, startEvent);
            }

            draggie.startPoint.x = event.gesture.center.pageX;
            draggie.startPoint.y = event.gesture.center.pageY;

            removalBinPosition.x = 0;
            removalBinPosition.y = $(document).height();

            Hammer.utils.stopEvent(event);
          }

          function handleDragMove(event) {
            if(isDragging) {
              elementCornerPosition.x = Math.max(draggie.position.x, 0);
              elementCornerPosition.y = Math.min(draggie.position.y + hmDesktopCardSize.height - mainContent[0].scrollTop, mainContent[0].clientHeight);
              removalBinDistance = Hammer.utils.getPointDistance(elementCornerPosition, removalBinPosition);

              if(removalBinDistance < 100) {
                setTimeout(function() {
                  item.placeRect.x = -500;
                  item.placeRect.y = -500;
                }, 1);
                activateBin();
              } else {
                deactivateBin();
              }

              Hammer.utils.stopEvent(event);
            }
          }

          function handleDragEnd(event) {
            isDragging = false;
            isInteracting = false;
            scrollableContainer.css({'-ms-scroll-limit': ''});

            if(isBinActive) {
              draggie.isEnabled = false;
              hmAnimationService.requestAnimation('bin-detach');
              activePageService.detachCard(scope.card, true);
            }
            deactivateBin();

            if(event.gesture.pointerType !== 'mouse') {
              interactionStop();
            }
          }

          function activateBin() {
            if( ! isBinActive) {
              isBinActive = true;

              innerElement
              .clearQueue('touchFeedback')
              .velocity('stop')
              .velocity({
                transformOriginX: [ '50%', '50%' ],
                transformOriginY: [ '50%', '50%' ],
              }, {
                duration: 0, queue: false
              })
              .velocity({
                transformOriginX: '50%',
                transformOriginY: '50%',
                scale: .75,
                rotateZ: -23
              }, {
                easing: 'ease',
                duration: 500,
                queue: 'touchFeedback'
              })
              .dequeue('touchFeedback');

              removalBin
              .clearQueue('binAnimation')
              .velocity('stop')
              .velocity({
                scale: 3,
                translateX: 10,
                translateY: -15,
                rotateZ: 10
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'binAnimation'
              })
              .dequeue('binAnimation');

              removalBinTop
              .clearQueue('binTopAnimation')
              .velocity('stop')
              .velocity({
                transformOriginX: '20%',
                transformOriginY: '40%',
                rotateZ: -20
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'binTopAnimation'
              })
              .dequeue('binTopAnimation');

            }
          }

          function deactivateBin() {
            if(isBinActive) {
              isBinActive = false;

              innerElement
              .clearQueue('touchFeedback')
              .velocity('stop')
              .velocity('reverse', {
                queue: 'touchFeedback'
              })
              .velocity({
                scale: 1,
                rotateZ: 0
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'touchFeedback'
              })
              .dequeue('touchFeedback');

              removalBin
              .clearQueue('binAnimation')
              .velocity('stop')
              .velocity({
                scale: 1,
                translateX: 0,
                translateY: 0,
                rotateZ: 0
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'binAnimation'
              })
              .dequeue('binAnimation');

              removalBinTop
              .clearQueue('binTopAnimation')
              .velocity('stop')
              .velocity({
                rotateZ: 0
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'binTopAnimation'
              })
              .dequeue('binTopAnimation');

            }
          }

          function interactionStart() {
            // Stop interaction indication if drag did not start
            if(interactionDragTimeout) {
              $timeout.cancel(interactionDragTimeout);
            }
            interactionDragTimeout = $timeout(function timeout() {
              if( ! isDragging) {
                interactionStop();
              }
            }, hammer.options.holdTimeout + 10);

            if(innerElement.data('velocity') && innerElement.data('velocity').isAnimating) {
              innerElement
              .clearQueue('touchFeedback')
              .velocity('stop')
              .velocity({
                rotateY: [ 30, 0 ]
              }, {
                //easing: [1,0,.8,1],
                easing: [0,.25,1,0],
                duration: hammer.options.holdTimeout,
                queue: 'touchFeedback'
              })
              .velocity({
                transformOriginX: [ '50%', '100%' ],
                rotateY: [ 0, 30 ],
                translateX: [ '10%', 0 ],
                translateZ: [ 100, 0 ],
                scale: 1,
                rotateZ: 0
              }, {
                easing: 'ease',
                duration: 200,
                queue: 'touchFeedback'
              })
              .dequeue('touchFeedback');
            }
            else {
              innerElement
              .velocity({
                transformPerspective: [ 500, 500 ],
                transformOriginX: [ '100%', '100%' ],
                transformOriginY: [ '50%', '50%' ],
                transformOriginZ: [ 0, 0 ],
                translateX: [ 0, 0 ],
                translateZ: [ 0, 0 ]
              }, {
                duration: 0,
                queue: false
              })
              .velocity({
                rotateY: [ 30, 0 ]
              }, {
                //easing: [1,0,.8,1],
                easing: [0,.25,1,0],
                duration: hammer.options.holdTimeout,
                queue: 'touchFeedback'
              })
              .velocity({
                transformOriginX: [ '50%', '100%' ],
                rotateY: [ 0, 30 ],
                translateX: [ '10%', 0 ],
                translateZ: [ 100, 0 ],
                scale: 1,
                rotateZ: 0
              }, {
                easing: 'ease',
                duration: 300,
                queue: 'touchFeedback'
              })
              .dequeue('touchFeedback');
            }
          }

          function interactionStop() {
            innerElement
            .clearQueue('touchFeedback')
            .velocity('stop')
            .velocity({
              rotateY: 0,
              translateX: 0,
              translateZ: 0,
              scale: 1,
              rotateZ: 0
            }, {
              duration: 200,
              easing: 'ease',
              queue: 'touchFeedback'
            })
            .velocity({
              transformPerspective: [ 500, 500 ],
              transformOriginX: [ '50%', '50%' ],
              transformOriginY: [ '50%', '50%' ],
              transformOriginZ: [ 0, 0 ]
            }, {
              duration: 0,
              queue: 'touchFeedback'
            })
            .dequeue('touchFeedback');
          }

        }
      };
    }]);

  // Directives for dragging elements into hmPackery
  hmDesktop.controller('hmPackerySatelliteCtrl', ['$scope', '$element', '$attrs',
  function($scope, $element, $attrs) {
    
  }]);

  hmDesktop.directive('hmPackerySatellite', ['$parse', '$timeout', 'hmCardActionService', function($parse, $timeout, hmCardActionService) {
    return {
      restrict: 'A',
      controller: 'hmPackerySatelliteCtrl',
      link: function linkingFn(scope, element, attrs) {
        // Init after the main hmPackery scope exists
        var init = scope.$root.$watch('hmPackeryScope', function(hmPackeryScope) {
          var hammer, desktopItem, target, targetScope, lastEvent, scrollableContainer, mainContent,
              isDragging, isItemAdded, isItemAddHandled, isMouseHold, isTouchDrag;
          
          mainContent = angular.element('.main-content');
          scrollableContainer = element.closest('.scrollable');

          if (!(hammer = element.data('hammer'))) {
            hammer = Hammer(element[0]);
            element.data('hammer', hammer);
          }

          hammer.on('tap', handleTap);
          hammer.on('dragstart hold', handleDragStart);
          hammer.on('drag', handleDragMove);
          hammer.on('dragend release', handleDragEnd);

          scope.$on('$destroy', function() {
            hammer.off('tap', handleTap);
            hammer.off('dragstart hold', handleDragStart);
            hammer.off('drag', handleDragMove);
            hammer.off('dragend release', handleDragEnd);
          });

          hmPackeryScope.$watchCollection('itemsById', function() {
            if(isItemAdded === false) {
              isItemAdded = true;
              startDesktopDrag();
            }
          });

          function handleTap(event) {
            target = angular.element(event.gesture.startEvent.target).closest('[hm-packery-satellite-item]');
            if(target.length > 0) {
              targetScope = target[0].hmPackerySatelliteItemScope;
              target = target[0].hmPackerySatelliteElement;
              hmCardActionService.handleCardAction(event, targetScope.card);
            }
          }

          function startDesktopDrag() {
            var unregisterFn;
            desktopItem = hmPackeryScope.itemsById[targetScope.card.id];
            var desktopItemScope = desktopItem.element[0].cardScope;
            unregisterFn = desktopItemScope.$on('cardTemplateLoaded', handleCardTemplateLoaded);
            function handleCardTemplateLoaded() {
              // Start dragging attached card from the middle at the last event position
              desktopItem.element[0].style.left = (lastEvent.gesture.center.pageX - hmDesktopCardSize.width / 2) + 'px';
              desktopItem.element[0].style.top = (lastEvent.gesture.center.pageY + mainContent[0].scrollTop - hmDesktopCardSize.height / 2) + 'px';
              desktopItem.dragStart(lastEvent);
              scope.activeDrawer = 0;
              unregisterFn();
            }
          }

          function handleDragStart(event) {
            lastEvent = event;

            // We want to use the hold event for touch and drag event for mouse
            isMouseHold = event.type === 'hold' && event.gesture.pointerType == 'mouse';
            isTouchDrag = event.type === 'dragstart' && event.gesture.pointerType != 'mouse';
            if(isMouseHold || isTouchDrag) {
              return;
            }

            scrollableContainer.css({'-ms-scroll-limit': '0 0 0 0'});

            target = angular.element(event.gesture.startEvent.target).closest('[hm-packery-satellite-item]');
            if(target.length > 0) {
              isDragging = true;
              targetScope = target[0].hmPackerySatelliteItemScope;
              target = target[0].hmPackerySatelliteElement;

              if(scope.isCardInCurrentPage(targetScope.card)) {
                //scope.$apply(startDesktopDrag);
              } else {
                isItemAdded = false;
                scope.attachCard(targetScope.card);
              }

              Hammer.utils.stopEvent(event);
            }
          }

          function handleDragMove(event) {
            lastEvent = event;
            if(isDragging) {
              if(desktopItem) {
                desktopItem.dragMove(event);
              }
              Hammer.utils.stopEvent(event);
            }
          }

          function handleDragEnd(event) {
            if(isDragging && desktopItem) {
              scrollableContainer.css({'-ms-scroll-limit': ''});
              desktopItem.dragEnd(event);
              isDragging = false;
            }
          }

        init()});
      }
    };
  }]);

  hmDesktop.directive('hmPackerySatelliteItem', ['$parse', '$timeout', function($parse, $timeout) {
    return {
      restrict: 'A',
      require: '^hmPackerySatellite',
      link: function linkingFn(scope, element, attrs) {
        var hmPackeryScope = scope.$root.hmPackeryScope;

        element[0].hmPackerySatelliteElement = element;
        element[0].hmPackerySatelliteItemScope = scope;

      }
    };
  }]);

  hmDesktop.animation('.hm-desktop-card', ['hmAnimationService', function(hmAnimationService) {
    var scope, draggie, item, drawers = angular.element('.drawer');
    return {
      enter: function enter(element, done) {
        scope = element.scope();

        if(hmAnimationService.isAnimationRequested('attach')) {
          element
          .velocity({
            scale: [ 0, 0 ],
            opacity: [ 0, 0 ]
          }, {
            duration: 0,
            queue: false,
          })
          .velocity({
            scale: [ 1, 0 ],
            opacity: [ 1, 0 ]
          }, {
            easing: 'easeOutBack',
            complete: done
          });
        }
        else if(hmAnimationService.isAnimationRequested('page-enter')) {
          item = scope.pckry.getItem(element[0]);
          element.css({opacity: 0});
          element.velocity('transition.perspectiveLeftIn', {
            delay: (Math.max(item.position.x, item.position.y) + Math.min(item.position.x, item.position.y)),
            duration: 1000,
            complete: done
          });
        }
        else {
          done();
        }
      },
      leave: function leave(element, done) {
        scope = element.scope();
        draggie = element.data('draggie');

        removeFrom(scope.pckry.getItem(element[0]), scope.pckry.items);
        scope.pckry._resetLayout();
        scope.pckry._manageStamps();

        if(hmAnimationService.isAnimationRequested('bin-detach')) {
          element
          .velocity({
            translateX: [ draggie.dragPoint.x - 100, draggie.dragPoint.x ],
            translateY: [ draggie.dragPoint.y + 100, draggie.dragPoint.y ],
            scale: [ 0, 1 ],
            opacity: [ 0, 1 ]
          }, {
            easing: 'ease',
            duration: 400,
            complete: function() {
              done();
              scope.pckry.layout();
            }
          });
        }
        else if(hmAnimationService.isAnimationRequested('detach')) {
          element
          .velocity({
            translateX: [ draggie.dragPoint.x, draggie.dragPoint.x ],
            translateY: [ draggie.dragPoint.y, draggie.dragPoint.y ],
            scale: [ 0, 1 ],
            opacity: [ 0, 1 ]
          }, {
            easing: 'easeInBack',
            complete: function() {
              done();
              scope.pckry.layout();
            }
          });
        }
        else {
          scope.pckry.layoutItems(scope.pckry.items, true);
          done();
        }
      }
    };
  }]);

})(window, window.angular, _);
