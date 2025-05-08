const socket = io('/overview');

socket.on('connect', () => {
    console.log('Connected to /overview');
});

socket.on('backendData', (data) => {
    console.log('Received from server:', data);

    // PROCESS DATA HERE

});

function init() {
    go.Diagram.licenseKey = "288647e1b4614fc702d90676423d6bbc5cf07e34ca960ef60a0013f4e95b6b40759bbc7854db8dc4d4ea5efa482d95d98d96397ec44a0c3be138d7d845ea86fde23073b0110e178dac5371c7cbad2ca2ff7e76a7c2e022a68928d9f2eba8c19958b8a0874ecf5ab97b7d54370177a819bef98c69e904991f6d6dcaf7fbfbbf4afb6f729b9ee54888ea";
    myDiagram = new go.Diagram('myDiagramDiv', {
      'animationManager.isEnabled': false,
      'undoManager.isEnabled': true,
      "rotatingTool.snapAngleMultiple": 90,
      "rotatingTool.snapAngleEpsilon": 45
    });

    // This sample defines several custom Shape geometries
    const tank1 = 'F M 0 0 L 0 75 25 100 50 75 50 0z' // 50x100 sized-shape
    const tank2 = 'F M 0 0 L 0 100 10 100 10 90 40 90 40 100 50 100 50 0z' // 50x100 sized-shape
    const tank3 = 'F M 0 100 L 0 25 A 25 25 0 0 1 50 25 L 50 100 z' // 50x100 sized-shape

    const labelLeft = 'F M 0 20 L 30 40 100 40 100 0 30 0 z'
    const labelRight = 'F M 0 0 L 70 0 100 20 70 40 0 40 z'

    const valve = 'F1 M0 0 L40 20 40 0 0 20z M20 10 L20 30 M12 30 L28 30';
    const pump = 'F M 8 10 A 2 2 0 1 1 6 8 L 9 8 L 9 10 Z M 5 11 A 1 1 0 0 1 7 9';
    const sensor = 'F M 0 0 L 15 15 L 15 20 L 5 20 L 5 15 L 0 15 L 0 10 L -2 10 L -2 4 L 0 4 Z';

    const colors = {
      black: '#151c26',
      white: '#ffffff',
      gray: '#2c323b',
      green: '#7ba961',
      blue: '#00a9b0',
      pink: '#e483a2',
      yellow: '#f9c66a',
      orange: '#e48042',
      red: '#ed2d44'
    }

    const textDefaults = { font: '10px InterVariable, sans-serif', stroke: colors.white };

    // Tanks have a variable number of connection ports.
    // Each port must specify its location on the tank (alignment spot)
    // And potentially its fromSpot or toSpot
    const tankPort = new go.Panel()
      .bind('alignment', 'a')
      .bind('portId', 'p')
      .bind('fromSpot', 'fs')
      .bind('toSpot', 'ts')
      .add(new go.Shape("Diamond", { width: 10, height: 10, fill: colors.white }));

    // Base template is a shape with a label
    myDiagram.nodeTemplateMap.add('',
      // Outer spot panel holding inner spot panel (main element) and ports
      new go.Node('Spot', {
        itemTemplate: tankPort
      })
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .bind('itemArray', 'ports')
        .add(
          // Inner spot panel holding Shape and Text label
          new go.Panel('Spot')
            .add(
              new go.Shape({
                geometryString: tank1,
                strokeWidth: 1,
                stroke: 'gray',
                width: 75, height: 140,
                fill: new go.Brush('Linear', {
                  0: go.Brush.darken(colors.white),
                  0.2: colors.white,
                  0.33: go.Brush.lighten(colors.white),
                  0.5: colors.white,
                  1: go.Brush.darken(colors.white),
                  start: go.Spot.Left,
                  end: go.Spot.Right
                })
              })
                .bind('width')
                .bind('height')
                .bind('geometryString', 'tankType'),
              // tank label
              new go.TextBlock({
                font: 'bold 13px InterVariable, sans-serif',
                stroke: colors.black
              }).bind('text', 'key')
            )
        )
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
        selectionObjectName: "SHAPE", rotatable: true
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
            geometryString: valve,
            strokeWidth: 2,
            portId: "", fromSpot: new go.Spot(1, 0.35), toSpot: new go.Spot(0, 0.35)
          })
          .bind('fill', 'color')
          .bind('stroke', 'color', (c) => go.Brush.darkenBy(c, 0.3))
        )
    );

    myDiagram.nodeTemplateMap.add("pump",
      new go.Node("Vertical", {
        locationSpot: new go.Spot(0.5, 1, 0, -21), locationObjectName: "SHAPE",
        selectionObjectName: "SHAPE", rotatable: true
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
          .bind('fill', 'color')
          .bind('stroke', 'color', (c) => Brush.darkenBy(c, 0.3))
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
        new go.Shape({ width: 18, height: 18, fill: colors.white }).bind('fill'),
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
    myDiagram.nodeTemplateMap.add("sensor",
      new go.Node("Vertical")
        .bindTwoWay("location", "pos", go.Point.parse, go.Point.stringify)
        .add(
          new go.Panel("Horizontal", { margin: 4 })
            .add(
              new go.Shape({ fill: colors.black, stroke: colors.white, strokeWidth: 2, geometryString: sensor, portId: '', fromSpot: new go.Spot(0, 0.4, 0, 0) }),
              new go.TextBlock({ margin: 2 }).set(textDefaults).bind('text', 'key')
            ),
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
        toShortLength: 3
      })
        .bind('fromEndSegmentLength', 'fromEndSeg')
        .bind('toEndSegmentLength', 'toEndSeg')
        .add(
          new go.Shape({ strokeWidth: 8, stroke: colors.black, isPanelMain: true }),
          new go.Shape({ strokeWidth: 3.5, stroke: colors.green, isPanelMain: true })
            .bind('stroke', 'color'),
          new go.Shape({ stroke: colors.green, fill: colors.green, toArrow: 'Triangle' })
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

    myDiagram.linkTemplateMap.add('sensor',
      new go.Link({
        layerName: 'Background'
      })
        .add(
          new go.Shape({ strokeWidth: 1.5, stroke: colors.red, strokeDashArray: [2, 2] })
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
          {key: 'VakuumPump', category: 'pump', color: colors.gray, pos: "450 300"},

          // TANKS
          {
            key: 'Vakuum-\nChamber', tankType: tank3, color: colors.black, pos: "100 150", ports: [
              { p: 'OUT1', fs: go.Spot.RightSide, a: new go.Spot(1, 0.5) },
            ]
          },
         
          // VALVES
          { key: 'Valve', category: 'valve', color: colors.red, pos: "300 150" },

          // SENSORS:
          { key: 'Pressure', category: 'sensor', value: '100', pos: "200 165", unit: 'mbar' },

          // MONITOR PANELS
          {
            key: 'cTCV102', title: 'Monitor TCV102', category: 'monitor', pos: "32 35",
            values: [
              { label: 'SV', unit: '°C', value: '12.0' },
              { label: 'PV', unit: '°C', value: '12.0' },
              { label: 'OP', unit: '%', value: '25.0' }
            ],
            statuses: [
              { fill: colors.red },
              { fill: colors.green },
              { fill: colors.green }
            ]
          },
        ],
      linkDataArray:
        [
          { from: 'Vakuum-\nChamber', to: 'Valve', color: colors.red, fromPort: 'OUT1' },
          { from: 'Valve', to: 'VakuumPump', color: colors.red },
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