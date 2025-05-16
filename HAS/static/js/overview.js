const socket = io();

var isFusionMode = true;
var HV_U = 0;
var HV_f = 0;
var HV_PWM = 0;
var HV_ON = true;
var Pump_ON = true;
var ValvePOS = 0;

socket.on('newDataAvailable', function(data) {
  console.log('Received message:', data.data);
  isFusionMode = data.data
  const nodeData = myDiagram.model.findNodeDataForKey("Tank1"); // oder ein anderer Key
  myDiagram.startTransaction("refresh node");
  myDiagram.model.updateTargetBindings(nodeData);
  myDiagram.commitTransaction("refresh node");
});

function init() {

    go.Diagram.licenseKey = "288647e1b4614fc702d90676423d6bbc5cf07e34ca960ef60a0013f4e95b6b40759bbc7854db8dc4d4ea5efa482d95d98d96397ec44a0c3be138d7d845ea86fde23073b0110e178dac5371c7cbad2ca2ff7e76a7c2e022a68928d9f2eba8c19958b8a0874ecf5ab97b7d54370177a819bef98c69e904991f6d6dcaf7fbfbbf4afb6f729b9ee54888ea";
    myDiagram = new go.Diagram('myDiagramDiv', {
      'animationManager.isEnabled': false,
      'undoManager.isEnabled': true,
      "rotatingTool.snapAngleMultiple": 90,
      "rotatingTool.snapAngleEpsilon": 45
    });

    console.log(isFusionMode);
    // This sample defines several custom Shape geometries
    const tank1 = 'F M 0 0 L 0 75 25 100 50 75 50 0z' // 50x100 sized-shape
    const tank2 = 'F M 0 0 L 0 100 10 100 10 90 40 90 40 100 50 100 50 0z' // 50x100 sized-shape
    const tank3 = 'F M 0 100 L 0 25 A 25 25 0 0 1 50 25 L 50 100 z' // 50x100 sized-shape

    const labelLeft = 'F M 0 20 L 30 40 100 40 100 0 30 0 z'
    const labelRight = 'F M 0 0 L 70 0 100 20 70 40 0 40 z'

    const valve = 'F1 M0 0 L40 20 40 0 0 20z M20 10 L20 30 M12 30 L28 30';
    const pump = 'F M 8 10 A 2 2 0 1 1 6 8 L 9 8 L 9 10 Z M 5 11 A 1 1 0 0 1 7 9';
    const sensorBAR = 'F M 0 0 A 10 10 0 1 1 0 20 A 10 10 0 1 1 0 0 M 0 10 L 6 4 M -1 20 L -1 28 L 1 28 L 1 20 Z';
    const sensorTEMP = 'F M 0 0 L 0 20 A 2 2 0 1 0 0 24 A 2 2 0 1 0 0 20 Z';

    const colors = {
      black: '#151c26',
      white: '#ffffff',
      gray: '#2c323b',
      green: '#7ba961',
      blue: '#00a9b0',
      pink: '#e483a2',
      yellow: '#f9c66a',
      orange: '#e48042',
      red: '#ed2d44',
      violet: '#8A2BE2',
      lightblue: '#ADD8E6',
    }

    const textDefaults = { font: '10px InterVariable, sans-serif', stroke: colors.white };

    // Tanks have a variable number of connection ports.
    // Each port must specify its location on the tank (alignment spot)
    // And potentially its fromSpot or toSpot
    const tankPort1 = new go.Panel()
      .bind('alignment', 'a')
      .bind('portId', 'p')
      .bind('fromSpot', 'fs')
      .bind('toSpot', 'ts')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    const tankPort2 = new go.Panel()
      .bind('alignment', 'a2')
      .bind('portId', 'p2')
      .bind('fromSpot', 'fs2')
      .bind('toSpot', 'ts2')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    const tankPort3 = new go.Panel()
      .bind('alignment', 'a3')
      .bind('portId', 'p3')
      .bind('fromSpot', 'fs3')
      .bind('toSpot', 'ts3')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    const tankPort4 = new go.Panel()
      .bind('alignment', 'a4')
      .bind('portId', 'p4')
      .bind('fromSpot', 'fs4')
      .bind('toSpot', 'ts4')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    const tankPort5 = new go.Panel()
      .bind('alignment', 'a5')
      .bind('portId', 'p5')
      .bind('fromSpot', 'fs5')
      .bind('toSpot', 'ts5')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    const tankPort6 = new go.Panel()
      .bind('alignment', 'a6')
      .bind('portId', 'p6')
      .bind('fromSpot', 'fs6')
      .bind('toSpot', 'ts6')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));




    myDiagram.nodeTemplateMap.add('',
      new go.Node('Spot')
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .bind('itemArray', 'ports')
        .add(
          new go.Panel('Spot')
            .add(
              new go.Shape({
                geometryString: tank1,
                strokeWidth: 1,
                stroke: 'gray',
                width: 75,
                height: 140
              })
                .bind('width')
                .bind('height')
                .bind('geometryString', 'tankType')
                .bind(
                  new go.Binding('fill', '', function (data) {
                    return isFusionMode
                      ? new go.Brush('Linear', {
                          0: go.Brush.darken(colors.white),
                          0.2: colors.pink,
                          0.33: go.Brush.lighten(colors.pink),
                          0.5: colors.pink,
                          1: go.Brush.darken(colors.white),
                          start: go.Spot.Left,
                          end: go.Spot.Right
                        })
                      : new go.Brush('Linear', {
                          0: go.Brush.darken(colors.white),
                          0.2: colors.white,
                          0.33: go.Brush.lighten(colors.white),
                          0.5: colors.white,
                          1: go.Brush.darken(colors.white),
                          start: go.Spot.Left,
                          end: go.Spot.Right
                        });
                  }).ofObject()
                ),
              new go.TextBlock({
                font: 'bold 13px InterVariable, sans-serif',
                stroke: colors.black
              }).bind('text', 'key')
            )
        )
        .add(tankPort1)
        .add(tankPort2)
        .add(tankPort3)
        .add(tankPort4)
        .add(tankPort5)
        .add(tankPort6)
    );


    myDiagram.nodeTemplateMap.add('label',
      new go.Node('Auto')
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(
          new go.Shape({
            portId: '',
            fromSpot: go.Spot.Right, toSpot: go.Spot.LeftRightSides,
            geometryString: labelRight,
            strokeWidth: 4,
            // width: 100, height: 40,
            fill: colors.black
          })
            .bind('width')
            .bind('height')
            .bind('geometryString', 'direction', (d) => d === 'right' ? labelRight : labelLeft)
            .bind('stroke', 'color'),
          new go.TextBlock({
            margin: new go.Margin(8, 40, 8, 8),
            textAlign: 'center',
            font: '12px sans-serif',
            stroke: colors.white,
            alignment: new go.Spot(0.1, 0.5)
          })
            .bind('margin', 'direction', (d) => d === 'right' ? new go.Margin(8, 40, 8, 8) : new go.Margin(8, 8, 8, 40))
            .bind('alignment', 'direction', (d) => d === 'right' ? new go.Spot(0.3, 0.5) : new go.Spot(0.7, 0.5))
            .bind('text')
        ));

        myDiagram.nodeTemplateMap.add("valve",
          new go.Node("Vertical", {
            locationSpot: new go.Spot(0.5, 1, 0, -21), locationObjectName: "SHAPE",
            selectionObjectName: "SHAPE", rotatable: false
          })
            
            .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
            .add(
              new go.TextBlock({
                background: colors.black,
                alignment: go.Spot.Center,
                textAlign: "center",
                margin: 2,
                editable: true
              })
                .set(textDefaults)
                .bind("text", 'key'),
                
              new go.Shape({
                name: "SHAPE",
                geometryString: valve,
                strokeWidth: 2,
                portId: "", fromSpot: new go.Spot(1, 0.35), toSpot: new go.Spot(0, 0.35)
              })
                .bind('fill', 'ValvePOS', v =>
                  v === 0 ? colors.gray :
                  v === 1 ? colors.blue :
                  colors.lightblue // Zwischenstellung
                )
                .bind('stroke', 'ValvePOS', v =>
                  v === 0 ? colors.gray :
                  v === 1 ? colors.blue : colors.blue // Zwischenstellung
                ),
              new go.TextBlock({
                  margin: new go.Margin(4, 0, 0, 0),
                  textAlign: "center"})
                  .set(textDefaults)
                  .bind("text", "ValvePOS", v => v.toFixed(2)) // zwei Kommastellen

            )
        );

    myDiagram.nodeTemplateMap.add("pump",
      new go.Node("Vertical", {
        locationSpot: new go.Spot(0.5, 1, 0, -21), locationObjectName: "SHAPE",
        selectionObjectName: "SHAPE", rotatable: false
      })
        .bindTwoWay("angle")
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(
          new go.TextBlock({
            background: colors.black,
            alignment: go.Spot.Center,
            textAlign: "center",
            margin: 2,
            editable: true
          })
            .set(textDefaults)
            .bind("text", 'key')
            // keep the text upright, even when the whole node has been rotated upside down
            .bindObject("angle", "angle", a => a === 180 ? 180 : 0),
          new go.Shape({
            name: "SHAPE",
            geometryString: pump,
            width: 45, height: 40,
            strokeWidth: 2,
            portId: "", fromSpot: new go.Spot(1, 0.25), toSpot: new go.Spot(0, 0.5)
          })
            .bind('fill', '', function(data) {
                return isFusionMode ? colors.blue : colors.gray;
            })
            .bind('stroke', 'color', (c) => go.Brush.darkenBy(c, 0.3))  

        )
          

        
    );

    // This is a component of the "monitor" node template
    const valuesTableItem = new go.Panel('TableRow')
      .add(
        new go.TextBlock("").set(textDefaults).bind('text', 'label'),
        new go.Panel("Spot", { column: 1 })
          .add(
            new go.Shape({ stroke: colors.orange, fill: colors.black, margin: 2, width: 40, height: 15 }),
            new go.TextBlock("", {}).set(textDefaults).bind('text', 'value')
          ),
        new go.TextBlock("", { column: 2, alignment: go.Spot.Left }).set(textDefaults).bind('text', 'unit')
      )
    const valuesTable = new go.Panel("Table", { strech: go.Stretch.Horizontal, itemTemplate: valuesTableItem })
      .bind('itemArray', 'values');

    // This is a component of the "monitor" node template, showing a dynamic number of status blocks
    const statusPanelTemplate = new go.Panel('Spot')
      .add(
        new go.Shape({ width: 30, height: 18, fill: colors.white }).bind('fill'),
        new go.TextBlock().set(textDefaults).bind('text')
      )
    const statusPanel = new go.Panel("Horizontal", {
      width: 90, height: 20,
      itemTemplate: statusPanelTemplate
    }).bind('itemArray', 'statuses')


    // Monitor node for monitoring values, linked to a pump or valve
    myDiagram.nodeTemplateMap.add("monitor",
      new go.Node("Auto")
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(
          new go.Shape({ fill: colors.black, stroke: colors.white, strokeWidth: 2 }),
          new go.Panel("Vertical", { margin: 4 })
            .add(
              // Title
              new go.TextBlock("Title", { strech: go.Stretch.Horizontal }).set(textDefaults).bind('text', 'title'),
              // Notifications
              statusPanel,
              // Values
              valuesTable
            )
        )
    );

    // Sensor node, linked to a tank
    myDiagram.nodeTemplateMap.add("sensorBAR",
      new go.Node("Vertical", {locationObjectName: "SHAPE",
        selectionObjectName: "SHAPE", rotatable: false}
      )
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(

              
          new go.Panel("Spot", { margin: 1 },)
            .bind("angle")
            .add(
              new go.Shape({
                name: "SHAPE",
                geometryString: sensorBAR,
                strokeWidth: 2,
                portId: "", fromSpot: new go.Spot(0.5, 1), toSpot: new go.Spot(0, 0.35)
                  }),
              new go.Shape({ fill: colors.black, stroke: colors.white, strokeWidth: 2, geometryString: sensorBAR}),                  
            ),
            
          new go.TextBlock({ margin: 2 }).set(textDefaults).bind('text', 'key'),

          new go.Panel("Horizontal")
            .add(
              new go.Panel("Spot", { column: 1 })
                .add(
                  new go.Shape({ stroke: colors.orange, fill: colors.black, margin: 2, width: 40, height: 15 }),
                  new go.TextBlock("", {}).set(textDefaults).bind('text', 'value')
                ),
              new go.TextBlock("", { column: 2, alignment: go.Spot.Left }).set(textDefaults).bind('text', 'unit')
              
            ),
 
        )
      
    );

        // Sensor node, linked to a tank
    myDiagram.nodeTemplateMap.add("sensorTEMP",
      new go.Node("Horizontal", {locationObjectName: "SHAPE",
        selectionObjectName: "SHAPE", rotatable: false})
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(
          new go.Panel("Spot",)
            .bind("angle")
            .add(
              new go.Shape({
                name: "SHAPE",
                geometryString: sensorTEMP,
                strokeWidth: 2,
                portId: "", fromSpot: new go.Spot(0.5, 0.1)
                  }),
              new go.Shape({ fill: colors.black, stroke: colors.white, strokeWidth: 2, geometryString: sensorTEMP}),
            ),

          new go.TextBlock({ margin: 2 }).set(textDefaults).bind('text', 'key'),
          new go.Panel("Horizontal")
            .add(
              new go.Panel("Spot", { column: 1 })
                .add(
                  new go.Shape({ stroke: colors.orange, fill: colors.black, margin: 2, width: 40, height: 15 }),
                  new go.TextBlock("", {}).set(textDefaults).bind('text', 'value')
                ),
              new go.TextBlock("", { column: 2, alignment: go.Spot.Left }).set(textDefaults).bind('text', 'unit')
            )
        )
    );


    myDiagram.linkTemplateMap.add('',
      new go.Link({
        routing: go.Routing.AvoidsNodes, corner: 12, layerName: 'Background',
        toShortLength: 3, relinkableFrom: false, relinkableTo: false
    
      })
        .bind('fromEndSegmentLength', 'fromEndSeg')
        .bind('toEndSegmentLength', 'toEndSeg')
        .add(         
          new go.Shape({ strokeWidth: 3.5, isPanelMain: true })
            .bind('stroke', 'color')
            .bind('strokeWidth'),
          new go.Shape({toArrow: 'Triangle'})
            .bind('stroke', 'color')
            .bind('fill', 'color'),
          // Link label, invisible unless text is specified
          new go.Panel('Auto', { visible: false })
            .bind('visible', 'text', (t) => true)
            .add(
              new go.Shape('RoundedRectangle', { strokeWidth: 1, fill: colors.gray }),
              new go.TextBlock({ margin: new go.Margin(3,1,1,1) }).set(textDefaults).bind('text')
          )
        )
    )

    myDiagram.linkTemplateMap.add('monitor',
      new go.Link({
        curve: go.Curve.Bezier, layerName: 'Background',
        fromSpot: go.Spot.Top, fromEndSegmentLength: 30
      })
        .bind('fromSpot', 'fs')
        .bind('toSpot', 'ts')
        .add(
          new go.Shape({ strokeWidth: 3, stroke: colors.white, strokeDashArray: [3, 4], isPanelMain: true })
            .bind('stroke', 'color')
        )
    )



    myDiagram.model = new go.GraphLinksModel({
      copiesArrays: true,
      copiesArrayObjects: true,
      linkFromPortIdProperty: 'fromPort',
      linkToPortIdProperty: 'toPort',
      nodeDataArray:
        [
          //PUMP
          {key: 'VakuumPump', category: 'pump', color: colors.gray, angle: 180 ,pos: "450 215"},

          // TANKS
          {
            key: 'Vakuum-\nChamber', tankType: tank3, color: colors.yellow, pos: "150 150", ports: [
              { p: 'PumpPort', a: new go.Spot(1, 0.5) },
              { p2: 'HVPort', a2: new go.Spot(0.5, 0) },
              { p3: 'ValvePort', a3: new go.Spot(0, 0.5) },
              { p4: 'TempPortIN', a4: new go.Spot(0.9, 0.9) },
              { p5: 'PressurePort', a5: new go.Spot(0.5, 1) },
              { p6: 'TempPortOUT', a6: new go.Spot(1, 0.25) },
            ] 
          },

          // VALVES
          { key: 'Valve', category: 'valve', angle: 180, ValvePOS: ValvePOS, pos: "100 226" },

          // Druck-SENSORS:
          { key: 'Pressure', category: 'sensorBAR', value: '100', angle: 180, pos: "204.5 360", unit: 'mbar'},

          // Temperatur-SENSORS Außen:
          { key: 'OUT Temperature', category: 'sensorTEMP', value: '10', angle: 270, pos: "260 193.75", unit: '°C' },

          // Temperatur-SENSORS Innen:
          { key: 'IN Temperature', category: 'sensorTEMP', value: '10',angle: 270, pos: "260 285", unit: '°C' },

          // MONITOR PANELS
          {
            key: 'HV-Modul', title: 'HV-Modul', category: 'monitor', pos: "143.5 -40",
            values: [
              { label: 'f', unit: 'Hz', value: HV_f },
              { label: 'U', unit: 'V', value: HV_U },
              { label: 'PWM', unit: '%', value: HV_PWM }
            ],
            statuses: [
               { fill: (HV_ON ? colors.green : colors.red) }
            ]
          },
        ],
      linkDataArray:
        [
          { from: 'VakuumPump', to: 'Vakuum-\nChamber', toPort: 'PumpPort', color: Pump_ON ? colors.blue: colors.gray},
          { from: 'HV-Modul', to: 'Vakuum-\nChamber', toPort: 'HVPort',color: HV_ON ? colors.yellow: colors.gray},
          { from: 'IN Temperature', to: 'Vakuum-\nChamber', toPort: 'TempPortIN',color: colors.white,strokeWidth: 2},
          { from: 'OUT Temperature', to: 'Vakuum-\nChamber', toPort: 'TempPortOUT',color: colors.white, strokeWidth: 2},
          { from: 'Valve', to: 'Vakuum-\nChamber', toPort: 'ValvePort',color: colors.gray},
          { from: 'Pressure', to: 'Vakuum-\nChamber', toPort:'PressurePort', color: colors.white},
          

        ]
    }
    ); // end model assignment

    // Simulate data coming in to the monitor
    // This randomly assigns new data to the itemArrays in the monitor nodes
    // and the data in the sensor nodes
    /*
    setInterval(() => {
      myDiagram.commit(() => {
        const sensorKeys = ['S1', 'S2'].map(k => myDiagram.findNodeForKey(k))
        for (const n of sensorKeys) {
          const d = n.data;
          myDiagram.model.set(d, 'value', roundAndFloor(parseFloat(d.value) + random(-0.5, 0.55), 1));
        }
      }, null); // null tells the Diagram to skip the undo manager

      if (+new Date % 2 === 0) return; // do the updates below half as often
      myDiagram.commit(() => {
        const controlNodes = ['cTCV102', 'cFCV101', 'cFM102', 'cFM103'].map(k => myDiagram.findNodeForKey(k))
        for (const n of controlNodes) {
          const vals = n.data.values;
          myDiagram.model.set(vals[0], 'value', roundAndFloor(parseFloat(vals[0].value) + random(-0.5, 0.55), 1));
          myDiagram.model.set(vals[1], 'value', roundAndFloor(parseFloat(vals[1].value) + random(-0.3, 0.35), 1));
          myDiagram.model.set(vals[2], 'value', roundAndFloor(parseFloat(vals[2].value) + random(-0.2, 0.2), 1));
        }
      }, null); // null tells the Diagram to skip the undo manager

      // rarely, randomly change a monitor color block
      if (+new Date % 15 === 0) return;
      myDiagram.commit(() => {
        const controlNodes = ['cTCV102', 'cFCV101', 'cFM102', 'cFM103'].map(k => myDiagram.findNodeForKey(k))
        for (const n of controlNodes) {
          const vals = n.data.statuses;
          myDiagram.model.set(vals[0], 'fill', Math.random() > 0.5 ? colors.green : colors.white)
          myDiagram.model.set(vals[1], 'fill', Math.random() > 0.5 ? colors.yellow : colors.white);
        }
      }, null); // null tells the Diagram to skip the undo manager
    // }, 550);
    */


  } // end init
  window.click = function () {

  };

  document.addEventListener('DOMContentLoaded', init);