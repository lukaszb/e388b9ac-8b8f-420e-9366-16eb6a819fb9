import Button from './components/Button.js'
import { sleep } from './utils.js'


const { defineComponent, toRefs, reactive } = Vue


export default defineComponent({
  name: 'PageCollectionList',
  template: `

    <div class="my-4 flex items-center space-x-4">
      <h1 class="font-semibold text-gray-400">Collections</h1>
    </div>

    <div class="my-4">
      <Button :loading="isCollectionListCreateInProgress" @click="createCollection()">Fetch new collection</Button>
    </div>

    <ul role="list" class="divide-y divide-gray-200">
      <li
        v-for="collection in collections"
        :key="collection.id"
        class="py-3"
      >
        <router-link
          :to="collection.id"
          class="text-blue-400 hover:text-yellow-400"
        >
          {{ formatDate(collection.date) }}
        </router-link>
      </li>
    </ul>

  `,
  components: {
    Button,
  },
  setup() {
    const state = reactive({
      isCollectionListCreateInProgress: false,
      collections: [],
      isCollectionsFetchInProgress: false,
    })
    const handleClick = () => {
      state.isCollectionListCreateInProgress = !state.isCollectionListCreateInProgress
    }


    const fetchCollections = async () => {
      state.isCollectionsFetchInProgress = true
      state.collections = await wretch('/api/collections').get().json()
      state.isCollectionsFetchInProgress = true
    }

    fetchCollections()


    const createCollection = () => {
      state.isCollectionListCreateInProgress = true
      // const request = wretch('/api/collections/create').post().
      wretch('/api/collections/create').post({}).res(async res => {

        // user should feel like this action does something in the background
        // even if it fast, so let's make a minimum time return response
        await sleep(750)
        const json = await res.json()
        await fetchCollections()
        state.isCollectionListCreateInProgress = false
      })
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleString('en-US', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
    }

    return {
      ...toRefs(state),
      handleClick,

      createCollection,
      formatDate,
    }
  }
})
