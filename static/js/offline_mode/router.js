let OfflineModeRouter = function(controller, offlineModePage) {
   "use strict";

   let routes = {
      '#ovc_home': controller.ovcHome,
      '#ovc_view': controller.ovcView,
      '#ovc_form1a': controller.ovcForm1a
   };

   let router = (routes) => {
      return  (url) => {
         let pageUrl = url.split('/')[0];
         offlineModePage.removeClass('visible');

         if (routes[pageUrl]) {
            routes[pageUrl]();
         } else {
            controller.ovcErrorPage();
         }
      }
   };

   return {
      route: (url) => router(routes)(url)
   }
};
