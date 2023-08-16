<template>
  <div class="window">
    <div class="chatWindow">
      <h1>AGPT</h1>
      <h3>Бесплатный доступ к языковым моделям / Free access to language models</h3>
       <div>
         <p>Языковая модель: / Language model:</p>
        <select v-model="model" class="selectModel">
          <option value="g35t">GPT 3.5 Turbo</option>
          <option value="g4">GPT 4</option>
        </select>
      </div>
      <div>
        <div v-for="(message, index) in messages" :key="index">
          <pre style="white-space: pre-wrap;">{{ message }}</pre>
          <hr>
        </div>
        <textarea class="ipt1" v-model="personality" placeholder="Базовый промпт / Base prompt" :disabled="isSending"></textarea><br>
        <textarea class="ipt2" v-model="message" placeholder="Напишите свой промпт здесь / Your prompt here" :disabled="isSending" @keyup.enter="sendMessage"></textarea><br>
        <button class="btn" :disabled="isSending" @click="sendMessage">{{ sendButtonLabel }}</button><br>
        <button class="btn" id="btn2" :disabled="isSending" @click="clearContext">Очистить контекст / Clear context</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      model: 'g35t',
      messages: [],
      personality: '',
      message: '',
      context: '',
      isSending: false,
      sendButtonLabel: 'Отправить / Send'
    }
  },
  methods: {
    async sendMessage(event) {
      if (event.shiftKey) {
        return;
      }
      this.isSending = true
      this.sendButtonLabel = 'Отправка / Sending'
      let address
      if (this.model == 'g35t') {
        address = 'http://localhost:1010/chat35t'
      } else if (this.model == 'g4') {
        address = 'http://localhost:1010/chat4'
      }
      const response = await axios.post(address, {
        prompt: this.message,
        context: this.context,
        personality: this.personality,
      });
      const data = response.data;
      console.log(data);
      this.message = "You: " + this.message
      this.context = data.context
      this.messages.push(this.message)
      this.messages.push("AGPT: " + data.response)
      this.message = ''
      this.isSending = false
      this.sendButtonLabel = 'Отправить / Send'
    },
    async clearContext() {
      location.reload();
    }
  }
}
</script>


<style>
  h1, h1, h3, h4, h5, p, pre {
    font-family: 'Roboto', sans-serif;
    word-wrap: break-word;
  }
  .window {
    display: grid;
    place-items: center;
    margin-top: 20dvh;
    margin-left: 10px;
    margin-right: 10px;
  }
  .btn {
    margin-top: 10px;
    padding: 3px;
    border-radius: 7px;
  }
  .ipt2 {
    padding: 3px;
    border-radius: 7px;
    width: 300px;
    height: 130px;
  }
  .ipt1 {
    padding: 3px;
    border-radius: 7px;
    width: 200px;
    height: 15px;
  }
  .selectModel {
    margin-bottom: 20px;
  }
</style>