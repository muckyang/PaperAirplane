const requireAuth = () => (from, to, next) => {
  const isAuthenticated = false
  if (isAuthenticated) return next()
  next('/login?returnPath=userinfo')
}

export default [
  {
    path: "/info",
    view: "Info",
    name: "info"
  },
  {
    path: "/",
    view: "Home",
    name: "home"
  },
  {
    path: "/myRoute",
    view: "MyRoute",
    name: "myroute"
  },
  {
    path: "/foodsearch",
    view: "FoodSearch",
    name: "foodsearch"
  },
  {
    path: "/toursearch",
    view: "TourSearch",
    name: "toursearch"
  },
  {
    path: "/customize",
    view: "Customize",
    name: "customize"
  },
  {
    path: "/rank",
    view: "Rank",
    name: "rank"
  },
  {
    path: "/recommend",
    view: "Recommend",
    name: "recommend"
  },
  {
    path: "/login",
    view: "user/Login",
    name: "login"
  },
  {
    path: "/register",
    view: "user/Register",
    name: "register"
  },
  {
    path: "/userinfo",
    view: "user/UserInfo",
    name: "userinfo",
    beforeEnter: requireAuth()
  },
];
