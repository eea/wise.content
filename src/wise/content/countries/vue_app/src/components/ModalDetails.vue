<template>
  <div>
    <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <span class="modal-title">
              {{ item.Title }}
            </span>
            <button class="modal-default-button" @click="$emit('close')">
              ×
            </button>
          </div>
          <div style="clear:both"></div>
          <div class="modal-body-container">
            <div class="modal-body">
              <dl class="result-table">
                <template v-for="field in Object.keys(item.fields)" v-if="field">
                  <dt class="key"><span>{{ field }}</span></dt>
                  <dd class="value"><span><span>{{ item.fields[field] }}</span></span></dd>
                </template>
              </dl>
            </div>
          </div>
          <div style="clear:both"></div>
        </div>
      </div>
    </div>
    </transition>
  </div>
</template>

<script>

  export default {
    props: [ 'item' ],

    data() {
      return {
        showModal: false
      }
    }
  }

</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  overflow:hidden;
  max-width: 1000px;
  max-height: 600px;
  margin: 0px auto;
  /*  padding: 20px 30px;*/
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header {
  text-align: center;
}
.modal-header h3 {
  margin-top: 2rem;
  color: #42b983;
}

.modal-body {
  color: black;
  width:100%;
  height:400px;
  padding-right:0;
}
.modal-body-container {
  margin: 20px 0;
  width:100%;
  height:100%;
  overflow:auto;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

dl {
  box-sizing:border-box;
  overflow: hidden;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-flow: row wrap;
  flex-flow: row wrap;
}
dt.key {
  box-sizing:border-box;
  display:block;
  font-weight: bold;
  line-height: 1.42857143;
  width: 20rem;
  float: left;
  clear: left;
  border-bottom: 1px dotted #CCC;
  margin-top: .4rem;
}
dd.value {
  box-sizing:border-box;
  display:block;
  float: left;
  /*   max-width: 63.5rem;*/
  max-width:765px;
  margin-left: -1px;
  margin-top: .4rem;
  background-color: #EEE;
  padding: .4rem;
  padding-left: .6rem;
  max-height: 200px;
  overflow: auto;
  width: 100%;
  box-shadow: inset 1px 0 1px rgba(0,0,0,0.1);
  -ms-box-shadow: inset 1px 0 1px rgba(0,0,0,0.1);
  -moz-box-shadow: inset 1px 0 1px rgba(0,0,0,0.1);
  -webkit-box-shadow: inset 1px 0 1px rgba(0,0,0,0.1);
  -o-box-shadow: inset 1px 0 1px rgba(0,0,0,0.1);
}

.modal-default-button {
  font-size:30px;
  cursor: pointer;
  background-color: transparent;
  border: 0;
  -webkit-appearance: none;
}

.modal-title {
  color: #0071b3;
  font-weight:bold;
  font-size: 3rem;
}
</style>
