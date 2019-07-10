let OfflineModeRouter = function(controller, offlineModePage) {
   "use strict";

   let routes = {
      '#ovc_home': controller.ovcHome,
      '#ovc_view': controller.ovcView,
      '#ovc_form1a': controller.ovcForm1a
   };

   offlineModePage.hide();

   let router = (routes) => {
      return  (url) => {
         let pageUrl = url.split('/')[0];

         console.log("pageUrl", pageUrl);

         // hide all other pages
         offlineModePage.hide();

         if (routes[pageUrl]) {
            $(pageUrl).show();
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
