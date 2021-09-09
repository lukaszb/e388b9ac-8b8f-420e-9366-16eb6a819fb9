import PageCollectionList from './PageCollectionList.js'
import PageCollectionDetails from './PageCollectionDetails.js'
import PageCollectionDetailsValuesCount from './PageCollectionDetailsValuesCount.js'


const { createApp } = Vue

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: [
    { path: '', name: 'collectionList', component: PageCollectionList },
    { path: '/:collectionId', name: 'collectionDetails', component: PageCollectionDetails, props: true },
    { path: '/:collectionId/values-count', name: 'collectionValuesCount', component: PageCollectionDetailsValuesCount, props: true },
  ]
})


console.log(" => init")

const app = createApp({
  template: `

  <div class="bg-yellow-300 rounded p-2 mb-4">
    <p><router-link to="/"><span class="font-semibold text-gray-900 pr-2">Star Wars</span></router-link> Explorer</p>

  </div>

  <div class="p-2">
    <router-view/>
  </div>

  `,
  components: {
    PageCollectionList,
  },
})

app.use(router)
app.mount('#app')
