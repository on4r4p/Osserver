from conf.osserver_conf import *

Template_Head="""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <meta http-equiv="refresh" content="3600">
    <title>OSSEC Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="On4r4p">
    <link rel="icon" href="images/ordinateur1.png">
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link href="css/font-style.css" rel="stylesheet">
    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/dash-charts.js"></script>
    <script type="text/javascript" src="js/gauge.js"></script>
    <style type="text/css">

    .sender {
      margin-bottom: 0px !important;
   }

    .read {
      height: 48px !important;
     }

    .disk {
      top: 15px !important;
    text-shadow: 0px 1px 1px silver;
     }

    .alerts {
      margin-left: 90px !important;
  width: 10px;
   text-shadow: 0pt 1px 1px silver;
   }

    .h1 {
      font-size: 18px !important;
      font-weight: bold !important;
      text-shadow: 0pt 1px 1px #999999;
      margin-bottom: 0px;
      margin-top: 0px;
      padding-top: 0%;
      padding-left: 0px;

     }
    .hr {
       margin-bottom: 0px;
      }



body {
  padding-top: 60px;
  background: #1f1f1f none repeat scroll 0% 0%;
  font-family: "Open Sans", sans-serif;
}

h1 {
  font-family: "Raleway", sans-serif;
}

h3, h4, h5 {
  font-family: "Open Sans", sans-serif;
  font-weight: lighter;
}

h2 {
  font-size: 22px;
}

h3 {
  font-size: 46px;
  color: #b2c831;
}

h5 {
  color: #b2c831;
  margin-left: 5px;
}


.dash-unit {
  margin-bottom: 0%;
  padding-bottom: 0px;
  border: 1px solid #383737;
  background-image: url("../images/sep-half.png");
  background-color: #4f4f4f;
  color: white;
  height: 290px;
text-shadow: 0px 1px 1px #cccccc;
}

.dash-unit:hover {
  background-color: #4f4f4f;
box-shadow: 3px 3px 2px 0px #151515;
}

.dash-unit dtitle {
  font-size: 11px;
  text-transform: uppercase;
  color: white;
  margin: 8px;
  padding: 0px;
}

.dash-unit hr {
  border-width: 1px 0px 0px;
  border-style: dashed none none;
  border-color: #151515 currentcolor currentcolor;
  margin-top: 3px;
}

.dash-unit h1 {
  font-family: "Raleway", sans-serif;
  font-weight: 300;
  font-size: 20px;
  line-height: 2px;
  letter-spacing: 0px;
  color: white;
  padding-top: 10px;
  padding-left: 5px;
  margin-top: 2px;
  text-align: center;
}

.dash-unit h2 {
  font-family: "Open Sans", sans-serif;
  font-weight: bold;
  font-size: 30px;
  line-height: 26px;
  letter-spacing: 0px;
  color: white;
  padding-top: 10px;
  padding-left: 5px;
  margin-top: 2px;
  text-align: center;
}

.dash-unit h3 {
  font-weight: 300;
  font-size: 15px;
  line-height: 2px;
  letter-spacing: 0px;
  color: #b2c831;
  padding-top: 10px;
  padding-left: 5px;
  margin-top: 2px;
  text-align: center;
}

.dash-unit p {
  font-size: 14px;
  font-weight: 200;
  line-height: 16px;
  margin: 0px 0px 10px;
  padding: 5px;
}

.dash-unit h4 {
  padding-left: 5px;
  margin-top: 2px;
  font-size: 13px;
  font-weight: lighter;
  line-height: 1;
  letter-spacing: 0px;
  color: white;
}

.dash-unit bold {
  font-family: "Open Sans", sans-serif;
  font-size: 26px;
  font-weight: bold;
  color: white;
  vertical-align: middle;
}

.half-unit {
  margin-bottom: 30px;
  padding-bottom: 4px;
  border: 1px solid #383737;
  background-image: url("../images/sep-half.png");
  background-color: #3d3d3d;
  color: white;
  height: 130px;
text-shadow: 0px 1px 1px #cccccc;
}

.half-unit:hover {
  background-color: #4f4f4f;
box-shadow: 3px 3px 2px 0px #151515;
}

.half-unit dtitle {
  font-size: 10px;
  text-transform: uppercase;
  color: white;
  margin: 8px;
  padding: 0px;
}

.half-unit hr {
  border-width: 1px 0px 0px;
  border-style: dashed none none;
  border-color: #151515 currentcolor currentcolor;
  margin-top: 3px;
}

.half-unit h1 {
  font-family: "Raleway", sans-serif;
  font-weight: 300;
  font-size: 20px;
  line-height: 1;
  letter-spacing: 0px;
  color: white;
  padding-top: 10px;
  padding-left: 5px;
  margin-top: 2px;
  text-align: center;
}

.half-unit h4 {
  padding-left: 5px;
  margin-top: 2px;
  font-size: 13px;
  font-weight: lighter;
  line-height: 1;
  letter-spacing: 0px;
  color: white;
}

.half-unit bold {
  font-family: "Open Sans", sans-serif;
  font-size: 26px;
  font-weight: bold;
  color: white;
  vertical-align: middle;
}

.cont ok {
  color: #b2c831;
}

.cont bad {
  color: #fa1d2d;
}

.cont2 {
  text-align: center;
  margin-top: -15px;
  font-size: 12px;
  line-height: 7px;
}

.cont2 bold {
  font-size: 10px;
  font-weight: bold;
  color: #b2c831;
}

.text p {
  font-family: "Open Sans", sans-serif;
  margin-left: 8px;
  font-size: 14px;
  line-height: 18px;
}

.text grey {
  font-size: 11px;
  color: silver;
}

.thumbnail {
  border: 0px none;
  background: rgba(0, 0, 0, 0) none repeat scroll 0% 0%;
  text-align: center;
  height: 0px;
}

.modal-header {
  background-image: url("../images/sep-half.png");
  background-color: #4f4f4f;
  color: white;
}

input[type="submit"] {
  font-family: "Open Sans", sans-serif;
  font-size: 15px;
  background: #b2c831 none repeat scroll 0% 0%;
  color: white;
  border: medium none;
  padding: 8px 28px 10px 26px;
  border-radius: 4px;
}

input[type="text"], textarea {
  background: #cdcbcc none repeat scroll 0% 0%;
  font-size: 13px;
  display: block;
  width: 100%;
  border: medium none;
box-shadow: none;
  height: 30px;
  line-height: 18px;
  padding: 0px;
  text-indent: 18px;
  margin: 0px 0px 18px;
}

textarea {
  line-height: 18px;
  padding: 18px;
  width: 100%;
  text-indent: 0px;
}

.textarea-container {
  margin: 0px 18px;
}

.textarea-container textarea {
  margin-left: -18px;
}

#contact textarea {
  width: 100%;
  height: 45px;
}

.progress-bar {
  background-color: #b2c831;
}

.info-user {
  text-align: center;
  font-size: 24px;
  color: #b2c831;
}

.fs1 {
  padding: 5px;
  position: relative;
}

.fs1:hover {
  position: relative;
  color: white;
  cursor: pointer;
}

.fs2 {
  padding: 5px;
  position: relative;
  font-size: 35px;
  vertical-align: text-bottom;
}

digiclock {
  font-size: 30px;
  color: white;
  text-align: center;
  line-height: 60px;
  margin-left: auto;
}

.clockcenter {
  text-align: center;
}

.framemail {
  cursor: default;
}

.framemail .window {
  font-size: 0px;
  margin-top: -1px;
  overflow: hidden;
  margin-left: -18px;
}

.framemail .window .mail li {
  background-color: #3d3d3d;
  background-image: linear-gradient(rgba(255, 255, 255, 0.05), rgba(0, 0, 0, 0.05));
  border-top: 1px solid #888888;
  position: relative;
  margin-left: -18px;
}

.framemail .window .mail li:first-child {
  border-top: medium none;
}

.framemail .window .mail li:hover {
  background-color: #5d5b5b;
}

.framemail .window .mail li::after, .framemail .window .mail li::before {
  border-left: 8px solid transparent;
  border-top: 8px solid #ddff66;
  content: "";
  height: 0px;
  position: absolute;
  right: 0px;
  top: 0px;
  width: 0px;
}

.framemail .window .mail li::before {
  border-top-color: #bbbbbb;
  border-width: 9px;
}

.framemail .window .mail li:nth-child(2)::after {
  border-top-color: #fa1d2d;
}

.framemail .window .mail li i {
  display: inline-block;
  height: 48px;
  width: 6px;
}

.framemail .window .mail li .read {
  background-color: #dddddd;
}

.framemail .window .mail li .unread {
  background: #b2c831 none repeat scroll 0% 0%;
}

.framemail .window .mail li img {
  background: #819da2 none repeat scroll 0% 0%;
  border-radius: 2px;
  height: 36px;
  left: 12px;
  position: absolute;
  top: 6px;
  width: 36px;
}

.framemail .window .mail li p {
  font: 13px / 24px sans-serif;
  left: 56px;
  position: absolute;
  top: 3px;
}

.framemail .window .mail li .sender {
  color: #e9e8e8;
  font-weight: bold;
text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.5);
}

.framemail .window .mail li .message {
  color: #999999;
  overflow: hidden;
  text-overflow: ellipsis;
  top: 21px;
  white-space: nowrap;
}

.framemail .window .mail li .message strong {
  color: #999999;
}

.framemail .window .mail li .actions {
  height: 16px;
  position: absolute;
  right: 19px;
  text-align: right;
  top: 0px;
  width: 96px;
}

.framemail .window .mail li .actions img {
  background: rgba(0, 0, 0, 0) none repeat scroll 0% 0%;
  display: inline-block;
  height: 16px;
  margin-left: 6px;
  opacity: 0.1;
  position: relative;
  width: 16px;
}

.framemail .window .mail li:hover .actions img {
  opacity: 0.25;
}

.framemail .window .mail li .actions img:hover {
  opacity: 0.75;
}

#load {
  width: 11.313em;
  height: 11.313em;
  border-radius: 5px;
  background-position: center center;
  margin: auto;
}

#space {
  width: 11.313em;
  height: 11.313em;
  border-radius: 5px;
  background-position: center center;
  margin: auto;
}

.section-graph {
  position: relative;
  height: 130px;
  color: white;
  margin-bottom: 20px;
}

.section-graph .graph-info {
  z-index: 99;
  position: absolute;
  font-weight: bold;
  margin-top: 12px;
  margin-left: 21px;
  width: 100px;
}

.section-graph .graph-info .graph-arrow {
  width: 0px;
  height: 0px;
  margin-top: 18px;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid white;
  float: left;
}

.section-graph .graph-info .graph-info-big {
  font-size: 24px;
  float: left;
  margin-left: 3px;
}

.section-graph .graph-info .graph-info-small {
  font-size: 12px;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.5);
  clear: left;
  margin-left: 8px;
}

.info-aapl {
  text-align: center;
}

.info-aapl ul {
  margin-left: 30%;
}

.info-aapl li {
  margin: 0px 6px 0px 0px;
  display: block;
  width: 9px;
  height: 40px;
  background-color: #f5f0ec;
  float: left;
  position: relative;
}

.info-aapl li span {
  display: block;
  width: 9px;
  height: 40px;
  position: absolute;
  bottom: 0px;
}

.info-aapl li span.orange {
  background-color: #fa1d2d;
}

.info-aapl li span.green {
  background-color: #b2c831;
}

#jstwitter ul li {
  color: #bdbdbd;
  padding: 0.5em 0.75em;
}

#jstwitter ul {
  margin-left: 0px;
  list-style: outside none none;
}

#jstwitter:first-child {
  border-top: 0px none;
}

ul#jstwitter li a {
  font-size: 10px;
  font-style: italic;
  color: #666666;
  text-decoration: none;
}

.btnnew {
  border-right: 0px none #707070;
  border-top: 0px none #707070;
  border-bottom: 0px none #707070;
  display: inline;
  padding: 4px 12px;
  margin-bottom: 0px;
  font-size: 14px;
  line-height: 20px;
  color: #b2c831;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  background-color: #5a5a5a;
  background-repeat: repeat-x;
  border-radius: 4px;
box-shadow: 0px 1px 0px rgba(255, 255, 255, 0.2) inset, 0px 1px 2px rgba(0, 0, 0, 0.05);
  background-image: linear-gradient(to bottom, #707070, #707070);
}

.switch {
  position: relative;
  margin: 20px auto;
  height: 26px;
  width: 120px;
  background: rgba(0, 0, 0, 0.25) none repeat scroll 0% 0%;
  border-radius: 3px;
box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3) inset, 0px 1px rgba(255, 255, 255, 0.1);
}

.switch-label {
  position: relative;
  z-index: 2;
  float: left;
  width: 58px;
  line-height: 26px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
  text-align: center;
text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.45);
  cursor: pointer;
}

.switch-label:active {
  font-weight: bold;
}

.switch-label-off {
  padding-left: 2px;
}

.switch-label-on {
  padding-right: 2px;
}

.switch-input {
  display: none;
}

.switch-input:checked + .switch-label {
  font-weight: bold;
  color: rgba(0, 0, 0, 0.65);
text-shadow: 0px 1px rgba(255, 255, 255, 0.25);
transition: all 0.15s ease-out 0s;
}

.switch-input:checked + .switch-label-on ~ .switch-selection {
  left: 60px;
}

.switch-selection {
  display: block;
  position: absolute;
  z-index: 1;
  top: 2px;
  left: 2px;
  width: 58px;
  height: 22px;
  background: #b2c831 linear-gradient(to bottom, #b6c753, #b2c831) repeat scroll 0% 0%;
  border-radius: 3px;
box-shadow: 0px 1px rgba(255, 255, 255, 0.5) inset, 0px 0px 2px rgba(0, 0, 0, 0.2);
transition: left 0.15s ease-out 0s;
}

.switch-blue .switch-selection {
  background: #3aa2d0 linear-gradient(to bottom, #4fc9ee, #3aa2d0) repeat scroll 0% 0%;
}

.switch-yellow .switch-selection {
  background: #fa1d2d linear-gradient(to bottom, #f93e4b, #fa1d2d) repeat scroll 0% 0%;
}

#canvas {
  display: block;
  width: 150px;
  margin: 30px auto;
}

.accordion-group {
  border: 1px solid #222222;
}

.accordion-heading {
  background-color: #5a5a5a;
  background-repeat: repeat-x;
  border-radius: 4px;
box-shadow: 0px 1px 0px rgba(255, 255, 255, 0.2) inset, 0px 1px 2px rgba(0, 0, 0, 0.05);
  background-image: linear-gradient(to bottom, #707070, #707070);
}

a {
  color: #b2c831;
  text-decoration: none;
}

a:hover {
  color: #dff948;
  text-decoration: none;
}

#footerwrap {
  width: 100%;
  background: #262626 url("../images/sep-half.png") repeat scroll 0% 0%;
  padding-top: 25px;
  padding-bottom: 40px;
  border-top: 8px solid #1d1d1d;
  text-align: center;
}

#footerwrap p {
  color: white;
  font-size: 12px;
}

#external-events {
  padding: 0px 10px;
  border: 1px solid #8b8b8a;
  background-color: #8b8b8a;
  border-radius: 4px;
  text-align: left;
}

#external-events h4 {
  font-size: 16px;
  margin-top: 0px;
  padding-top: 1em;
}

.external-event {
  margin: 10px 0px;
  padding: 2px 4px;
  background: #b2c831 none repeat scroll 0% 0%;
  color: white;
  font-size: 0.85em;
  cursor: pointer;
}

#external-events p {
  margin: 1.5em 0px;
  font-size: 11px;
  color: #b2c831;
}

#external-events p input {
  margin: 0px;
  vertical-align: middle;
}

#calendar {
  width: 100%;
}

@media ( max-width : 360px ) {
  .fc-header {
    margin-top: 15px;
  }
  .fc-header-title h2 {
    font-size: 10px;
  }
  .fc-header-right {
    display: none;
  }
  @media (min-width: 767px) and (max-width: 768px) {
  .info-aapl ul { margin-left: 10px; float: left; }
  #load { margin-left: 5px; margin-right: 10px; }
  #space { margin-left: 5px; margin-right: 10px; }
}
  @media (min-width: 560px) and (max-width: 685px) {
  .info-aapl ul { margin-left: 40%; }
}
}







</style> <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>    <![endif]-->
    <!-- Google Fonts call. Font Used Open Sans & Raleway -->
    <link href="http://fonts.googleapis.com/css?family=Raleway:400,300" rel="stylesheet"
      type="text/css">
    <link href="http://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet"
      type="text/css">
 </head>
  <body>

    <script type="text/javascript" src="js/highcharts.js"></script>
    <script type="text/javascript" src="js/series-label.js"></script>
    <script type="text/javascript" src="js/exporting.js"></script>
    <script type="text/javascript" src="js/export-data.js"></script>
    <script type="text/javascript" src="js/accessibility.js"></script>
    <script type="text/javascript" src="js/boost.js"></script>

    <!-- NAVIGATION MENU -->
    <div class="navbar-nav navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header"> <button type="button" class="navbar-toggle"
            data-toggle="collapse" data-target=".navbar-collapse"> <span class="icon-bar"></span>
            <span class="icon-bar"></span> <span class="icon-bar"></span> </button>
          <a class="navbar-brand" href="index.html"><img src="images/ossec_logo30.png"
              alt=""> Ossec Dashboard</a> </div>
      </div>
    </div>
    <div class="container">"""
Template_Row1="""      <!-- FIRST ROW OF BLOCKS -->
      <div class="row">"""
Template_Profile="""        <!-- USER PROFILE BLOCK -->
        <div class="col-sm-3 col-lg-3">
          <div class="dash-unit"> <dtitle>Teamrocket.org</dtitle>
            <hr style="margin: 0px;">
            <div class="thumbnail"> <canvas id="canvas" width="300" height="300">
              </canvas> </div>
            <!-- /thumbnail -->
            <h1 style="margin-bottom: 0px; margin-top: 0px; padding-top: 0%; padding-left: 0px;"class="h1">PONYS'S SECRET HQ!</h1>
            <h3>Summary</h3>
            <br>
            <br>
            <div class="info-user" style="position: relative; top: 120px;"><a href="ordinateur1.html"> <img
                class="avatar" src="images/ordinateur1.png" alt="ordinateur1 is Online"></a> <img class="avatar"
                src="images/ordinateur2.png" alt="ordinateur2 is Offline"> <a href="ordinateur3.html"><img class="avatar"
                src="images/ordinateur3.png" alt="ordinateur3 is Online"></a> <a href="ordinateur4.html"><img class="avatar"
                src="images/ordinateur430.png" alt="ordinateur4 is Online"></a> <a href="ordinateur5.html"><img class="avatar" src="images/ordinateur5.png"
                alt="ordinateur5 is Online"></a>
          </div>
         </div>
        </div>"""


Template_DailyBlock="""
        <div class="col-sm-3 col-lg-3">
          <!-- Daily BLOCK -->
          <div class="half-unit"> <dtitle style="margin: 8px; height: auto; border-radius: 0px;">Daily
              global Counter</dtitle>
            <hr style="margin-bottom: 4px;">
            <div class="cont." style="font-size: 18px; line-height: 15px; text-align: center; visibility: visible;">"""

Template_DailyBlockEND="""            </div>
          </div>"""

Template_HourBlock="""
          <!-- Hour BLOCK -->
          <div class="half-unit"> <dtitle>Last Hour global counter</dtitle>
            <hr style="margin-bottom: 4px;">
            <div class="cont." style="font-size: 18px; line-height: 15px; text-align: center; visibility: visible;">

                       <p><bold style="font-size: 18px;">Alerts:</bold> """

Template_HourBlockEND="""
            </div>
          </div>
        </div>"""

Template_AlertBlock1="""
        <div class="col-sm-3 col-lg-3">
          <div class="dash-unit" style="height: auto;"> <dtitle style="text-align: left;">Current Alerts
              Level Stats</dtitle>
            <hr>

            <p style="text-decoration: underline overline; font-weight: bold; text-align: center;">Max Alert Level: """

Template_AlertBlock1END="""            </div>
          </div>"""

Template_AlertBlock2="""
        <div class="col-sm-3 col-lg-3">
          <div class="dash-unit" style="height: auto;"> <dtitle style="text-align: left;"> Yesterday Alerts
              Level Stats</dtitle>
            <hr>

            <p style="text-decoration: underline overline; font-weight: bold; text-align: center;">Max Alert Level: """

Template_AlertBlock2END="""
          </div>
        </div>"""

Template_ChartJs="""<script type="text/javascript"  src="js/ossechart.js"></script>"""

Template_Row2="""
      </div>
      <!-- /row -->
      <!-- Second ROW OF BLOCKS -->
      <div class="row">"""

Template_Health="""
        <div class="col-sm-3 col-lg-3">
          <div class="dash-unit"> <dtitle>Health checkup</dtitle>
            <hr>
            <div class="framemail">
              <div class="window">
                <ul class="mail">"""

Template_HealthEND ="""
                </ul>
              </div>
            </div>
          </div>
          <!-- /dash-unit --> </div>"""

Template_Row3part1="""
      </div>
      <br>
      <!-- /row -->"""
Template_Row3part2="""


      <!-- Third ROW OF BLOCKS -->
      <div class="row">"""

Template_Chart="""        <div class="col-sm-6">
           <div class="dash-unit">
              <dtitle>Overall Stats Chart</dtitle>
              <hr class="hr">
              <div id="ossechart"></div>
           </div>
       </div>
"""

#Template_ChartEND="""<p><h3>CHART END PLACEHOLDER</h3></p>"""


Template_Cam="""      <div class="row">
        <div class="col-sm-3 col-lg-3">
          <div class="dash-unit" style="height: auto;"> <dtitle>New cams files
              saved</dtitle>
            <hr style="margin-bottom: 4px;">
            <div class="cont." style="line-height: 15px; text-align: center; visibility: visible;">"""


Template_CamEND="""
            </div>
          </div>
        </div>
      </div>
      <br>"""

Template_Row4="""
      </div>
      <br>
      <!-- /rowEnd -->
      <!-- Forth ROW OF BLOCKS -->
      <div class="row">"""


Template_Accordeon="""        <!-- ACCORDION BLOCK -->
        <div class="col-sm-9 col-lg-3">
          <div class="dash-unit" style="height: auto; position: absolute;"> <dtitle>Alerts Received</dtitle>
            <hr>
            <div class="accordion" id="accordion2">"""

Template_AccordeonEND="""            </div>
            <!--/accordion --></div>
        </div>"""



Template_Tail="""
      </div<!-- /rowEnd -->
      <br>
  </body>
</html>"""

