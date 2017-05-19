define(['sources/selection/range_boundary_navigator'], function (rangeBoundaryNavigator) {

  describe("#getUnion", function () {
    describe("when the ranges completely overlap", function () {
      it("returns a list with that range", function () {
        var ranges = [[1, 4], [1, 4], [1, 4]];

        var union = rangeBoundaryNavigator.getUnion(ranges);

        expect(union).toEqual([[1, 4]]);
      });
    });

    describe("when the ranges all overlap partially or touch", function () {
      it("returns one long range", function () {
        var rangeBounds = [[3, 6], [1, 4], [7, 14]];

        var union = rangeBoundaryNavigator.getUnion(rangeBounds);

        expect(union).toEqual([[1, 14]]);
      });

      it("returns them in order from lowest to highest", function () {
        var rangeBounds = [[3, 6], [2, 3], [10, 12]];

        var union = rangeBoundaryNavigator.getUnion(rangeBounds);

        expect(union).toEqual([[2, 6], [10, 12]]);
      });

      describe("when one range completely overlaps another", function() {

        it("returns them in order from lowest to highest", function () {
          var rangeBounds = [[9, 14], [2, 3], [11, 13]];

          var union = rangeBoundaryNavigator.getUnion(rangeBounds);

          expect(union).toEqual([[2, 3], [9, 14]]);
        });
      });

      describe("when one range is a subset of another", function () {
        it("returns the larger range", function () {
          var rangeBounds = [[2, 6], [1, 14], [8, 10]];

          var union = rangeBoundaryNavigator.getUnion(rangeBounds);

          expect(union).toEqual([[1, 14]]);
        })
      })
    });

    describe("when the ranges do not touch", function () {
      it("returns them in order from lowest to highest", function () {
        var rangeBounds = [[3, 6], [1, 1], [8, 10]];

        var union = rangeBoundaryNavigator.getUnion(rangeBounds);

        expect(union).toEqual([[1, 1], [3, 6], [8, 10]]);
      });
    });
  });


  describe("#mapDimensionBoundaryUnion", function () {
    it("returns a list of the results of the callback", function () {
      var rangeBounds = [[0, 1], [3, 3]];
      var callback = function () {
        return 'hello';
      };
      var result = rangeBoundaryNavigator.mapDimensionBoundaryUnion(rangeBounds, callback);
      expect(result).toEqual(['hello', 'hello', 'hello']);
    });

    it("calls the callback with each index in the dimension", function () {
      var rangeBounds = [[0, 1], [3, 3]];
      var callback = jasmine.createSpy('callbackSpy');
      rangeBoundaryNavigator.mapDimensionBoundaryUnion(rangeBounds, callback);
      expect(callback.calls.allArgs()).toEqual([[0], [1], [3]]);
    });
  });

  describe("#mapOver2DArray", function () {
    var data, rowCollector, processCell;
    beforeEach(function () {
      data = [[0, 1, 2, 3], [2, 2, 2, 2], [4, 5, 6, 7]];
      processCell = function (rowIndex, columnIndex) {
        return data[rowIndex][columnIndex];
      };
      rowCollector = function (rowData) {
        return JSON.stringify(rowData);
      };
    });

    it("calls the callback for each item in the ranges", function () {
      var rowRanges = [[0, 0], [2, 2]];
      var colRanges = [[0, 3]];

      var selectionResult = rangeBoundaryNavigator.mapOver2DArray(rowRanges, colRanges, processCell, rowCollector);

      expect(selectionResult).toEqual(["[0,1,2,3]", "[4,5,6,7]"]);
    });

    describe("when the ranges are out of order/duplicated", function () {
      var rowRanges, colRanges;
      beforeEach(function () {
        rowRanges = [[2, 2], [2, 2], [0, 0]];
        colRanges = [[0, 3]];
      });

      it("uses the union of the ranges", function () {
        spyOn(rangeBoundaryNavigator, "getUnion").and.callThrough();

        var selectionResult = rangeBoundaryNavigator.mapOver2DArray(rowRanges, colRanges, processCell, rowCollector);

        expect(rangeBoundaryNavigator.getUnion).toHaveBeenCalledWith(rowRanges);
        expect(rangeBoundaryNavigator.getUnion).toHaveBeenCalledWith(colRanges);
        expect(selectionResult).toEqual(["[0,1,2,3]", "[4,5,6,7]"]);
      });
    });
  });

  describe("#rangesToCsv", function () {
    var data, columnDefinitions, ranges;
    beforeEach(function () {
      data = [[1, "leopard", "12"],
        [2, "lion", "13"],
        [3, "cougar", "9"],
        [4, "tiger", "10"]];
      columnDefinitions = [{name: 'id', pos: 0}, {name: 'animal', pos: 1}, {name: 'size', pos: 2}];
      ranges = [new Slick.Range(0, 0, 0, 2), new Slick.Range(3, 0, 3, 2)];
    });

    it("returns csv for the provided ranges", function () {

      var csvResult = rangeBoundaryNavigator.rangesToCsv(data, columnDefinitions, ranges);

      expect(csvResult).toEqual("1,'leopard','12'\n4,'tiger','10'");
    });

    describe("when there is an extra column with checkboxes", function () {
      beforeEach(function () {
        columnDefinitions = [{name: 'not-a-data-column'}, {name: 'id', pos: 0}, {name: 'animal', pos: 1}, {
          name: 'size',
          pos: 2
        }];
        ranges = [new Slick.Range(0, 0, 0, 3), new Slick.Range(3, 0, 3, 3)];

      });

      it("returns csv for the columns with data", function () {
        var csvResult = rangeBoundaryNavigator.rangesToCsv(data, columnDefinitions, ranges);

        expect(csvResult).toEqual("1,'leopard','12'\n4,'tiger','10'");
      });
    });
  });
});