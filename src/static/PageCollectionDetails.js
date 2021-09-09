import Button from './components/Button.js'
import { sleep } from './utils.js'
import { FIELD_NAMES } from './consts.js'
const { defineComponent, reactive, toRefs, computed } = Vue


export default defineComponent({
  name: 'PageCollectionDetails',
  template: `
  <div>
    <div class="my-4 flex items-center space-x-4">
      <router-link to="/"><h1 class="font-semibold text-gray-400">Collections</h1></router-link>
      <span class="text-gray-300">/</span>
      <h1 class="font-semibold text-gray-400">{{ collectionId }}</h1>
    </div>

    <router-link class="hover:text-yellow-400"
      :to="{ name: 'collectionValuesCount', params: { collectionId } }"
    >Values count</router-link>

    <table class="table-fixed text-xs">
      <thead>
        <tr>
          <th
            v-for="field in FIELD_NAMES"
            :key="field"
            class="py-2"
            :class="[ {date: 'w-28' }[field] ]"
          >
            {{ field }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in (items || [])"
          :key="index"
          :class="[ (index % 2) && 'bg-gray-200' ]"
        >
          <td
            v-for="field in FIELD_NAMES"
            :key="field"
            class="border border-gray-500 px-4 py-2 text-gray-600 font-light"
          >
            {{ item[field] }}
          </td>
        </tr>
      </tbody>

    </table>

    <Button
      v-if="canLoadMore"
      class="mt-8"
      @click="fetchMoreData()"
      :loading="isCollectionDataFetchInProgress"
    >Load more</Button>

  </div>
  `,
  components: {
    Button,
  },
  props: {
    collectionId: String,
  },
  setup(props) {
    const state = reactive({
      isCollectionFetchInProgress: false,
      isCollectionDataFetchInProgress: false,
      collection: { id: null, date: null, items_count: 0 },
      items: [],
      page: 1,
    })

    const canLoadMore = computed(() => {
      return state.items.length < state.collection.items_count
    })

    const fetchCollectionData = async (id, sleepFor=0) => {
      state.isCollectionDataFetchInProgress = true
      const { items } = await wretch(`/api/collections/${id}/data?page=${state.page}`).get().json()
      state.page += 1

      if (sleepFor) {
        await sleep(sleepFor)
      }
      state.items = [ ...state.items, ...items ]
      state.isCollectionDataFetchInProgress = false
      return items
    }

    const fetchCollection = async (id) => {
      state.isCollectionFetchInProgress = true
      const request = wretch(`/api/collections/${id}`).get().json()
      const collection = await request
      state.isCollectionFetchInProgress = false
      state.collection = collection
      return collection
    }

    const fetchMoreData = async () => {
      fetchCollectionData(props.collectionId, 500)
    }

    const initialFetch = async (id) => {
      fetchCollection(id)
      fetchCollectionData(id)
    }

    initialFetch(props.collectionId)


    return {
      ...toRefs(state),
      FIELD_NAMES,
      fetchMoreData,
      canLoadMore,
    }
  }
})
