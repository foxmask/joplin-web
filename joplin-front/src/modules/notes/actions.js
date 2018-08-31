import notesApi from './api'
import types from './types'

export const actions = {
  [types.NOTE_FETCH_ALL]: async ({ commit }) => {
    commit(types.NOTE_SET_ALL, await notesApi.fetchNotes())
  },

  [types.NOTE_FETCH_TAG]: async ({ commit }, tag) => {
    commit(types.NOTE_SET_ALL, await notesApi.fetchNotesByTag(tag))
  },

  [types.NOTE_FETCH_FOLDER]: async ({ commit }, folder) => {
    commit(types.NOTE_SET_ALL, await notesApi.fetchNotesByFolder(folder))
  },

  [types.NOTE_SET]: async ({ commit }, note) => {
    commit(types.NOTE_SET, note)
  },

  [types.NOTE_CREATE]: async ({ commit }, note) => {
    commit(types.NOTE_APPEND, await notesApi.createNote(note))
  },

  [types.NOTE_CHANGE]: async ({ commit }, note) => {
    console.log('inside notes.components.actions types.NOTE_CHANGE ')
    console.log(note)
    commit(types.NOTE_CHANGE, await notesApi.updateNote(note))
  },

  [types.NOTE_DELETE]: async ({ commit }, id) => {
    await notesApi.deleteNote(id)
    commit(types.NOTE_REMOVE, id)
  }
}

export default actions