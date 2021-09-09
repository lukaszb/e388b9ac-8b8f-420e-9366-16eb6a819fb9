import Button from './components/Button.js'
import { sleep } from './utils.js'
import { FIELD_NAMES } from './consts.js'
const { defineComponent, reactive, toRefs, computed } = Vue


export default defineComponent({
  name: 'PageCollectionDetailsValuesCount',
  template: `
  <div>
    <div class="my-4 flex items-center space-x-4">
      <router-link to="/"><h1 class="font-semibold text-gray-400 hover:text-yellow-400">Collections</h1></router-link>
      <span class="text-gray-300">/</span>

      <router-link
      :to="{ name: 'collectionDetails', params: { collectionId } }"
    >
      <h1 class="font-semibold text-gray-400 hover:text-yellow-400">{{ collectionId }}</h1>
    </router-link>
    <span class="text-gray-300">/</span>
    <h1 class="font-semibold text-gray-400">Values Count</h1>
    </div>

    <div class="my-4">
      <button
        v-for="field in FIELD_NAMES"
        :key="field"
        class="py-2 px-3 text-sm mr-2 text-sm rounded"
        @click="toggleField(field)"
        :class="[ isSelected(field) ? 'bg-yellow-300 hover:bg-yellow-400' : 'bg-gray-200 text-gray-500 hover:bg-gray-300' ]"
      >
        {{ field }}
      </button>
    </div>

    <div v-if="selectedFields.size < 2" class="bg-gray-200 rounded p-4">
      <p class=" text-sm text-red-400 font-light">Please choose at least two fields in order to see any results.</p>
    </div>
    <div v-else>
      <table class="table-fixed text-xs">
        <thead>
          <tr>
            <th
              v-for="field in dataFields"
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
            v-for="(item, index) in (data || [])"
            :key="index"
            :class="[ (index % 2) && 'bg-gray-200' ]"
          >
            <td
              v-for="field in dataFields"
              :key="field"
              class="border border-gray-500 px-4 py-2 text-gray-600 font-light"
            >
              {{ item[field] }}
            </td>
          </tr>
        </tbody>

      </table>
    </div>

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
      collection: { id: null, date: null, items_count: 0 },
      selectedFields: new Set(),
      isDataFetchInProgress: false,
      data: [],
    })

    const fetchCollection = async (id) => {
      state.isCollectionFetchInProgress = true
      const request = wretch(`/api/collections/${id}`).get().json()
      const collection = await request
      state.isCollectionFetchInProgress = false
      state.collection = collection
      return collection
    }

    fetchCollection(props.collectionId)

    const isSelected = (field) => {
      return state.selectedFields.has(field)
    }

    const fetchData = async () => {
      const id = props.collectionId
      const fields = Array.from(state.selectedFields).join(',')
      const url = `/api/collections/${id}/data/distinct?fields=${fields}`

      state.isDataFetchInProgress = true
      const request = wretch(url).get().json()
      state.data = await request
    }

    const toggleField = (field) => {
      if (state.selectedFields.has(field)) {
        state.selectedFields = new Set(Array.from(state.selectedFields).filter(f => f !== field))
      } else {
        state.selectedFields = new Set(Array.from(state.selectedFields).concat([field]))
      }

      if (state.selectedFields.size >= 2) {
        fetchData()
      } else {
        state.data = []
      }
    }

    const dataFields = computed(() => {
      return [ ...Array.from(state.selectedFields), "Count" ]
    })


    return {
      ...toRefs(state),
      FIELD_NAMES,
      isSelected,
      toggleField,
      dataFields,
    }
  }
})
