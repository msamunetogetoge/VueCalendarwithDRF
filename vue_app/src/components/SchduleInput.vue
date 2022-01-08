<template>
  <v-app>
    <v-card class="mx-auto" max-width="620">
      <v-card-text>
        <v-container>
          <v-form>
            <v-text-field v-model="TitleDisplay" label="タイトル">
            </v-text-field>
            <v-textarea v-model="PlanAboutDisplay" label="詳細"> </v-textarea>
            <v-row>
              <v-col cols="12" sm="3">
                <v-menu
                  ref="MenuDatePickerFrom"
                  v-model="MenuDatePickerFrom"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="PlanFromMonth"
                      label="Date"
                      prepend-icon="mdi-calendar"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="PlanFromMonth"
                    no-title
                    @input="MenuDatePickerFrom = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" sm="3">
                <v-menu
                  ref="MenuTimePickerFrom"
                  v-model="MenuTimePickerFrom"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="PlanFromTime"
                      label="From"
                      persistent-hint
                      prepend-icon="mdi-clock-time-four-outline"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-model="PlanFromTime"
                    :allowed-minutes="allowedStep"
                    v-if="MenuTimePickerFrom"
                    format="24hr"
                    @click:minute="$refs.MenuTimePickerFrom.save(PlanFromTime)"
                  ></v-time-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" sm="3">
                <v-menu
                  ref="MenuDatePickerTo"
                  v-model="MenuDatePickerTo"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="PlanToMonth"
                      label="Date"
                      prepend-icon="mdi-calendar"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="PlanToMonth"
                    no-title
                    @input="MenuDatePickerTo = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" sm="3">
                <v-menu
                  ref="MenuTimePickerTo"
                  v-model="MenuTimePickerTo"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="PlanToTime"
                      label="From"
                      prepend-icon="mdi-clock-time-four-outline"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-model="PlanToTime"
                    :allowed-minutes="allowedStep"
                    v-if="MenuTimePickerTo"
                    format="24hr"
                    @click:minute="$refs.MenuTimePickerTo.save(PlanToTime)"
                  ></v-time-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="teal accent-4" @click="putPlan">
          {{ message }}
        </v-btn>
        <v-btn text color="teal accent-4" @click="CloseScheduleInput">
          キャンセル
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  props: {
    PlanID: Number,
    PlanFrom: Date,
    PlanTo: Date,
    Title: String,
    PlanAbout: String,
  },
  data: () => ({
    MenuDatePickerFrom: false,
    MenuDatePickerTo: false,
    MenuTimePickerFrom: false,
    MenuTimePickerTo: false,
    // PlanID: 0,
    UserID: "test",
    // PlanFrom: new Date(),
    PlanFromMonth: "",
    PlanFromTime: "",
    // PlanTo: new Date(),
    PlanToMonth: "",
    PlanToTime: "",
    TitleDisplay: "",
    PlanAboutDisplay: "",
    colors: "",
    message: "",
  }),
  mounted: function () {
    if (this.Title === "") {
      this.message = "予定登録";
    } else {
      this.message = "予定更新";
    }
    this.PlanFromMonth = this.PlanFrom.toISOString().substr(0, 10);
    this.PlanFromTime = this.PlanFrom.toISOString().substr(11, 5);
    this.PlanToMonth = this.PlanTo.toISOString().substr(0, 10);
    this.PlanToTime = this.PlanTo.toISOString().substr(11, 5);
    this.TitleDisplay = this.Title;
    this.PlanAboutDisplay = this.PlanAbout;
  },
  watch: {
    // PlanFromが変更されたらmonth, timeも変更
    PlanFrom: function (val) {
      this.PlanFromMonth = val.toISOString().substr(0, 10);
      this.PlanFromTime = val.toISOString().substr(11, 5);
    },
    // PlanToが変更されたらmonth, timeも変更
    PlanTo: function (val) {
      this.PlanToMonth = val.toISOString().substr(0, 10);
      this.PlanToTime = val.toISOString().substr(11, 5);
    },
  },
  methods: {
    CloseScheduleInput() {
      this.$emit("close");
    },
    allowedStep: (m) => m % 10 === 0,
    putPlan() {
      let url = "http://localhost:8000/schedules_detail/";
      url += this.PlanID + "/";
      const PlanFrom = new Date(this.PlanFromMonth + "T" + this.PlanFromTime);
      const PlanTo = new Date(this.PlanToMonth + "T" + this.PlanToTime);
      let data = JSON.parse(
        JSON.stringify({
          PlanID: this.PlanID,
          UserID: this.UserID,
          PlanFrom: PlanFrom,
          PlanTo: PlanTo,
          Title: this.TitleDisplay,
          PlanAbout: this.PlanAboutDisplay,
          Color: this.Color,
        })
      );
      var vm = this;
      axios
        .put(url, data)
        .then(() => {
          // const event = response.data[0];
          // const first = new Date(event.PlanFrom);
          // const last = new Date(event.PlanTo);
          // const name = event.Title;
          // const color = event.Color;
          // const detail = event.PlanAbout;
          // this.Title = name;
          // this.PlanFrom = first;
          // this.PlanTo = last;
          // this.Color = color;
          // this.PlanAbout = detail;
        })
        .catch(function (error) {
          if (error.response) {
            // 要求がなされたとサーバがステータスコードで応答した
            // 2XXの範囲外
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            // 要求がなされたが、応答が受信されなかった
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            console.log(error.request);
          } else {
            // トリガーしたリクエストの設定に何かしらのエラーがある
            console.log("Error", error.message);
          }
          console.log(error.config);
        })
        .finally(function () {
          vm.$emit("close");
        });
    },
  },
};
</script>