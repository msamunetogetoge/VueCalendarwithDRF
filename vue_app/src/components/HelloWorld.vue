<template>
  <v-app id="app">
    <schdule-input
      v-if="OpenInput"
      v-bind:PlanID="PlanID"
      v-bind:Title="Title"
      v-bind:PlanAbout="PlanAbout"
      v-bind:PlanFrom="PlanFrom"
      v-bind:PlanTo="PlanTo"
      @close="CloseScheduleInput"
    ></schdule-input>
    <v-row class="fill-height" v-if="IsCalendarOpen">
      <v-col>
        <v-sheet height="64">
          <v-toolbar flat>
            <v-btn
              outlined
              class="mr-4"
              color="grey darken-2"
              @click="setToday"
            >
              Today
            </v-btn>
            <v-btn fab text small color="grey darken-2" @click="prev">
              <v-icon small> mdi-chevron-left </v-icon>
            </v-btn>
            <v-btn fab text small color="grey darken-2" @click="next">
              <v-icon small> mdi-chevron-right </v-icon>
            </v-btn>
            <v-toolbar-title v-if="$refs.calendar">
              {{ $refs.calendar.title }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn outlined color="grey darken-2" @click="OpenInput = true">
              新規作成
            </v-btn>
            <v-menu bottom right>
              <template v-slot:activator="{ on, attrs }">
                <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                  <span>{{ typeToLabel[type] }}</span>
                  <v-icon right> mdi-menu-down </v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="type = 'day'">
                  <v-list-item-title>Day</v-list-item-title>
                </v-list-item>
                <v-list-item @click="type = 'week'">
                  <v-list-item-title>Week</v-list-item-title>
                </v-list-item>
                <v-list-item @click="type = 'month'">
                  <v-list-item-title>Month</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-toolbar>
        </v-sheet>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            v-model="focus"
            color="primary"
            :events="events"
            :event-color="getEventColor"
            :type="type"
            @click:event="showEvent"
            @click:more="viewDay"
            @click:date="viewDay"
          ></v-calendar>
          <v-menu
            v-model="selectedOpen"
            :close-on-content-click="false"
            :activator="selectedElement"
            offset-x
          >
            <v-card color="grey lighten-4" min-width="350px" flat>
              <v-toolbar :color="selectedEvent.color" dark>
                <v-btn icon @click="editPlan(selectedEvent)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn icon>
                  <v-icon>mdi-heart</v-icon>
                </v-btn>
                <v-btn icon>
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </v-toolbar>
              <v-card-text>
                <span v-html="selectedEvent.detail"></span>
              </v-card-text>
              <v-card-actions>
                <v-btn text color="secondary" @click="selectedOpen = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
        </v-sheet>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
import axios from "axios";
import SchduleInput from "./SchduleInput";
export default {
  components: { SchduleInput },
  data: () => ({
    PlanID: 0,
    PlanFrom: new Date(),
    PlanTo: new Date(),
    PlanAbout: "",
    Title: "",
    OpenInput: false,
    IsCalendarOpen: true,
    msg: "",
    focus: "",
    type: "month",
    typeToLabel: {
      month: "Month",
      week: "Week",
      day: "Day",
    },
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    events: [],
    colors: [
      "blue",
      "indigo",
      "deep-purple",
      "cyan",
      "green",
      "orange",
      "grey darken-1",
    ],
    names: [
      "Meeting",
      "Holiday",
      "PTO",
      "Travel",
      "Event",
      "Birthday",
      "Conference",
      "Party",
    ],
  }),
  watch: {
    OpenInput: function (val) {
      this.IsCalendarOpen = !val;
      this.updatePlan();
    },
  },
  mounted() {
    this.updatePlan();
    this.$refs.calendar.checkChange();
  },
  methods: {
    CloseScheduleInput() {
      this.OpenInput = false;
      this.selectedOpen = false;
    },
    editPlan(selectedEvent) {
      this.PlanID = selectedEvent.planid;
      this.PlanAbout = selectedEvent.detail;
      this.Title = selectedEvent.name;
      this.PlanFrom = new Date(selectedEvent.start);
      this.PlanTo = new Date(selectedEvent.end);
      this.OpenInput = true;
    },
    viewDay({ date }) {
      this.focus = date;
      this.type = "day";
    },
    getEventColor(event) {
      return event.color;
    },
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    updatePlan() {
      axios.get("http://localhost:8000/schedules/").then((response) => {
        const events = [];
        const eventcounts = response.data.length;
        for (let i = 0; i < eventcounts; i++) {
          const event = response.data[i];
          const first = new Date(event.PlanFrom);
          const last = new Date(event.PlanTo);
          const name = event.Title;
          const color = event.Color;
          const detail = event.PlanAbout;
          const planid = event.PlanID;
          events.push({
            name: name,
            start: first,
            end: last,
            color: color,
            timed: true,
            detail: detail,
            planid: planid,
          });
        }
        this.events = events;
      });
    },
  },
};
</script>