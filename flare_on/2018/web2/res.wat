(module
  (type (;0;) (func (param i32 i32 i32 i32) (result i32)))
  (type (;1;) (func (param i32)))
  (type (;2;) (func))
  (type (;3;) (func (param i32 i32 i32 i32 i32) (result i32)))
  (type (;4;) (func (param i32 i32 i32) (result i32)))
  (import "env" "putc_js" (func (;0;) (type 1)))
  (func (;1;) (type 2))
  (func (;2;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 2
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 2
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      get_local 6
      i32.load offset=12
      set_local 33
      get_local 33
      get_local 32
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 34
      get_local 34
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 35
    get_local 35
    return)
  (func (;3;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 2
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 1
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 2
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      i32.const -1
      set_local 35
      get_local 34
      get_local 35
      i32.xor
      set_local 36
      get_local 6
      i32.load offset=12
      set_local 37
      get_local 37
      get_local 36
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 38
      get_local 38
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 39
    get_local 39
    return)
  (func (;4;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 3
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 2
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 3
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      get_local 6
      i32.load offset=20
      set_local 35
      get_local 35
      i32.load8_u offset=2
      set_local 36
      i32.const 255
      set_local 37
      get_local 36
      get_local 37
      i32.and
      set_local 38
      get_local 34
      get_local 38
      i32.xor
      set_local 39
      get_local 6
      i32.load offset=12
      set_local 40
      get_local 40
      get_local 39
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 41
      get_local 41
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 42
    get_local 42
    return)
  (func (;5;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 3
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 3
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 3
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      get_local 6
      i32.load offset=20
      set_local 35
      get_local 35
      i32.load8_u offset=2
      set_local 36
      i32.const 255
      set_local 37
      get_local 36
      get_local 37
      i32.and
      set_local 38
      get_local 34
      get_local 38
      i32.and
      set_local 39
      get_local 6
      i32.load offset=12
      set_local 40
      get_local 40
      get_local 39
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 41
      get_local 41
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 42
    get_local 42
    return)
  (func (;6;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 3
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 4
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 3
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      get_local 6
      i32.load offset=20
      set_local 35
      get_local 35
      i32.load8_u offset=2
      set_local 36
      i32.const 255
      set_local 37
      get_local 36
      get_local 37
      i32.and
      set_local 38
      get_local 34
      get_local 38
      i32.or
      set_local 39
      get_local 6
      i32.load offset=12
      set_local 40
      get_local 40
      get_local 39
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 41
      get_local 41
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 42
    get_local 42
    return)
  (func (;7;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 3
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 5
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 3
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=1
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      get_local 6
      i32.load offset=20
      set_local 35
      get_local 35
      i32.load8_u offset=2
      set_local 36
      i32.const 255
      set_local 37
      get_local 36
      get_local 37
      i32.and
      set_local 38
      get_local 34
      get_local 38
      i32.add
      set_local 39
      get_local 6
      i32.load offset=12
      set_local 40
      get_local 40
      get_local 39
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 41
      get_local 41
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 42
    get_local 42
    return)
  (func (;8;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    i32.const 3
    set_local 7
    get_local 6
    get_local 0
    i32.store offset=20
    get_local 6
    get_local 1
    i32.store offset=16
    get_local 6
    get_local 2
    i32.store offset=12
    get_local 6
    get_local 3
    i32.store offset=8
    get_local 6
    i32.load offset=16
    set_local 8
    get_local 7
    set_local 9
    get_local 8
    set_local 10
    get_local 9
    get_local 10
    i32.gt_u
    set_local 11
    get_local 11
    set_local 12
    block  ;; label = @1
      block  ;; label = @2
        get_local 12
        i32.eqz
        br_if 0 (;@2;)
        i32.const 105
        set_local 13
        get_local 6
        get_local 13
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 6
      set_local 14
      get_local 6
      i32.load offset=20
      set_local 15
      get_local 15
      i32.load8_u
      set_local 16
      get_local 6
      get_local 16
      i32.store8 offset=31
      get_local 6
      i32.load8_u offset=31
      set_local 17
      i32.const 255
      set_local 18
      get_local 17
      get_local 18
      i32.and
      set_local 19
      i32.const 15
      set_local 20
      get_local 19
      get_local 20
      i32.and
      set_local 21
      i32.const 255
      set_local 22
      get_local 21
      get_local 22
      i32.and
      set_local 23
      get_local 14
      set_local 24
      get_local 23
      set_local 25
      get_local 24
      get_local 25
      i32.ne
      set_local 26
      get_local 26
      set_local 27
      block  ;; label = @2
        get_local 27
        i32.eqz
        br_if 0 (;@2;)
        i32.const 112
        set_local 28
        get_local 6
        get_local 28
        i32.store offset=24
        br 1 (;@1;)
      end
      i32.const 0
      set_local 29
      i32.const 3
      set_local 30
      get_local 6
      i32.load offset=20
      set_local 31
      get_local 31
      i32.load8_u offset=2
      set_local 32
      i32.const 255
      set_local 33
      get_local 32
      get_local 33
      i32.and
      set_local 34
      get_local 6
      i32.load offset=20
      set_local 35
      get_local 35
      i32.load8_u offset=1
      set_local 36
      i32.const 255
      set_local 37
      get_local 36
      get_local 37
      i32.and
      set_local 38
      get_local 34
      get_local 38
      i32.sub
      set_local 39
      i32.const 255
      set_local 40
      get_local 39
      get_local 40
      i32.and
      set_local 41
      get_local 6
      i32.load offset=12
      set_local 42
      get_local 42
      get_local 41
      i32.store8
      get_local 6
      i32.load offset=8
      set_local 43
      get_local 43
      get_local 30
      i32.store
      get_local 6
      get_local 29
      i32.store offset=24
    end
    get_local 6
    i32.load offset=24
    set_local 44
    get_local 44
    return)
  (func (;9;) (type 3) (param i32 i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 5
    i32.const 64
    set_local 6
    get_local 5
    get_local 6
    i32.sub
    set_local 7
    get_local 7
    set_global 0
    i32.const 0
    set_local 8
    get_local 7
    get_local 0
    i32.store offset=52
    get_local 7
    get_local 1
    i32.store offset=48
    get_local 7
    get_local 2
    i32.store offset=44
    get_local 7
    get_local 3
    i32.store offset=40
    get_local 7
    get_local 4
    i32.store offset=36
    get_local 7
    get_local 8
    i32.store offset=32
    get_local 7
    i32.load offset=52
    set_local 9
    get_local 7
    get_local 9
    i32.store offset=28
    get_local 7
    get_local 8
    i32.store offset=24
    block  ;; label = @1
      loop  ;; label = @2
        i32.const 0
        set_local 10
        get_local 7
        i32.load offset=28
        set_local 11
        get_local 7
        i32.load offset=52
        set_local 12
        get_local 7
        i32.load offset=48
        set_local 13
        get_local 12
        get_local 13
        i32.add
        set_local 14
        get_local 11
        set_local 15
        get_local 14
        set_local 16
        get_local 15
        get_local 16
        i32.lt_u
        set_local 17
        get_local 17
        set_local 18
        get_local 10
        set_local 19
        block  ;; label = @3
          get_local 18
          i32.eqz
          br_if 0 (;@3;)
          get_local 7
          i32.load offset=24
          set_local 20
          get_local 7
          i32.load offset=40
          set_local 21
          get_local 20
          set_local 22
          get_local 21
          set_local 23
          get_local 22
          get_local 23
          i32.lt_u
          set_local 24
          get_local 24
          set_local 19
        end
        block  ;; label = @3
          get_local 19
          set_local 25
          i32.const 1
          set_local 26
          get_local 25
          get_local 26
          i32.and
          set_local 27
          get_local 27
          i32.eqz
          br_if 0 (;@3;)
          i32.const 7
          set_local 28
          get_local 7
          i32.load offset=28
          set_local 29
          get_local 29
          i32.load8_u
          set_local 30
          get_local 7
          get_local 30
          i32.store8 offset=63
          get_local 7
          i32.load8_u offset=63
          set_local 31
          i32.const 255
          set_local 32
          get_local 31
          get_local 32
          i32.and
          set_local 33
          i32.const 15
          set_local 34
          get_local 33
          get_local 34
          i32.and
          set_local 35
          get_local 7
          get_local 35
          i32.store8 offset=23
          get_local 7
          i32.load8_u offset=23
          set_local 36
          i32.const 255
          set_local 37
          get_local 36
          get_local 37
          i32.and
          set_local 38
          get_local 28
          set_local 39
          get_local 38
          set_local 40
          get_local 39
          get_local 40
          i32.le_s
          set_local 41
          get_local 41
          set_local 42
          block  ;; label = @4
            get_local 42
            i32.eqz
            br_if 0 (;@4;)
            i32.const 112
            set_local 43
            get_local 7
            get_local 43
            i32.store offset=56
            br 3 (;@1;)
          end
          i32.const 0
          set_local 44
          i32.const 15
          set_local 45
          get_local 7
          get_local 45
          i32.add
          set_local 46
          get_local 46
          set_local 47
          i32.const 8
          set_local 48
          get_local 7
          get_local 48
          i32.add
          set_local 49
          get_local 49
          set_local 50
          i32.const 0
          set_local 51
          i32.const 1024
          set_local 52
          get_local 7
          i32.load8_u offset=23
          set_local 53
          i32.const 255
          set_local 54
          get_local 53
          get_local 54
          i32.and
          set_local 55
          i32.const 2
          set_local 56
          get_local 55
          get_local 56
          i32.shl
          set_local 57
          get_local 52
          get_local 57
          i32.add
          set_local 58
          get_local 58
          i32.load
          set_local 59
          get_local 7
          get_local 59
          i32.store offset=16
          get_local 7
          get_local 51
          i32.store8 offset=15
          get_local 7
          get_local 44
          i32.store offset=8
          get_local 7
          i32.load offset=16
          set_local 60
          get_local 7
          i32.load offset=28
          set_local 61
          get_local 7
          i32.load offset=48
          set_local 62
          get_local 7
          i32.load offset=28
          set_local 63
          get_local 7
          i32.load offset=52
          set_local 64
          get_local 63
          get_local 64
          i32.sub
          set_local 65
          get_local 62
          get_local 65
          i32.sub
          set_local 66
          get_local 61
          get_local 66
          get_local 47
          get_local 50
          get_local 60
          call_indirect (type 0)
          set_local 67
          get_local 44
          set_local 68
          get_local 67
          set_local 69
          get_local 68
          get_local 69
          i32.ne
          set_local 70
          get_local 70
          set_local 71
          block  ;; label = @4
            get_local 71
            i32.eqz
            br_if 0 (;@4;)
            br 1 (;@3;)
          end
          get_local 7
          i32.load8_u offset=15
          set_local 72
          i32.const 255
          set_local 73
          get_local 72
          get_local 73
          i32.and
          set_local 74
          get_local 7
          i32.load offset=44
          set_local 75
          get_local 7
          i32.load offset=24
          set_local 76
          get_local 75
          get_local 76
          i32.add
          set_local 77
          get_local 77
          i32.load8_u
          set_local 78
          i32.const 24
          set_local 79
          get_local 78
          get_local 79
          i32.shl
          set_local 80
          get_local 80
          get_local 79
          i32.shr_u
          set_local 81
          get_local 74
          set_local 82
          get_local 81
          set_local 83
          get_local 82
          get_local 83
          i32.eq
          set_local 84
          get_local 84
          set_local 85
          block  ;; label = @4
            get_local 85
            i32.eqz
            br_if 0 (;@4;)
            get_local 7
            i32.load offset=32
            set_local 86
            i32.const 1
            set_local 87
            get_local 86
            get_local 87
            i32.add
            set_local 88
            get_local 7
            get_local 88
            i32.store offset=32
          end
          get_local 7
          i32.load offset=8
          set_local 89
          get_local 7
          i32.load offset=28
          set_local 90
          get_local 90
          get_local 89
          i32.add
          set_local 91
          get_local 7
          get_local 91
          i32.store offset=28
          get_local 7
          i32.load offset=24
          set_local 92
          i32.const 1
          set_local 93
          get_local 92
          get_local 93
          i32.add
          set_local 94
          get_local 7
          get_local 94
          i32.store offset=24
          br 1 (;@2;)
        end
      end
      get_local 7
      i32.load offset=28
      set_local 95
      get_local 7
      i32.load offset=52
      set_local 96
      get_local 7
      i32.load offset=48
      set_local 97
      get_local 96
      get_local 97
      i32.add
      set_local 98
      get_local 95
      set_local 99
      get_local 98
      set_local 100
      get_local 99
      get_local 100
      i32.ne
      set_local 101
      get_local 101
      set_local 102
      block  ;; label = @2
        block  ;; label = @3
          get_local 102
          i32.eqz
          br_if 0 (;@3;)
          i32.const 0
          set_local 103
          get_local 7
          i32.load offset=36
          set_local 104
          get_local 104
          get_local 103
          i32.store8
          br 1 (;@2;)
        end
        get_local 7
        i32.load offset=32
        set_local 105
        get_local 7
        i32.load offset=40
        set_local 106
        get_local 105
        set_local 107
        get_local 106
        set_local 108
        get_local 107
        get_local 108
        i32.ne
        set_local 109
        get_local 109
        set_local 110
        block  ;; label = @3
          block  ;; label = @4
            get_local 110
            i32.eqz
            br_if 0 (;@4;)
            i32.const 0
            set_local 111
            get_local 7
            i32.load offset=36
            set_local 112
            get_local 112
            get_local 111
            i32.store8
            br 1 (;@3;)
          end
          i32.const 1
          set_local 113
          get_local 7
          i32.load offset=36
          set_local 114
          get_local 114
          get_local 113
          i32.store8
        end
      end
      i32.const 0
      set_local 115
      get_local 7
      get_local 115
      i32.store offset=56
    end
    get_local 7
    i32.load offset=56
    set_local 116
    i32.const 64
    set_local 117
    get_local 7
    get_local 117
    i32.add
    set_local 118
    get_local 118
    set_global 0
    get_local 116
    return)
  (func (;10;) (type 0) (param i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 4
    i32.const 32
    set_local 5
    get_local 4
    get_local 5
    i32.sub
    set_local 6
    get_local 6
    set_global 0
    i32.const 0
    set_local 7
    i32.const 11
    set_local 8
    get_local 6
    get_local 8
    i32.add
    set_local 9
    get_local 9
    set_local 10
    i32.const 0
    set_local 11
    get_local 6
    get_local 0
    i32.store offset=24
    get_local 6
    get_local 1
    i32.store offset=20
    get_local 6
    get_local 2
    i32.store offset=16
    get_local 6
    get_local 3
    i32.store offset=12
    get_local 6
    get_local 11
    i32.store8 offset=11
    get_local 6
    i32.load offset=24
    set_local 12
    get_local 6
    i32.load offset=20
    set_local 13
    get_local 6
    i32.load offset=16
    set_local 14
    get_local 6
    i32.load offset=12
    set_local 15
    get_local 12
    get_local 13
    get_local 14
    get_local 15
    get_local 10
    call 9
    set_local 16
    get_local 7
    set_local 17
    get_local 16
    set_local 18
    get_local 17
    get_local 18
    i32.ne
    set_local 19
    get_local 19
    set_local 20
    block  ;; label = @1
      block  ;; label = @2
        get_local 20
        i32.eqz
        br_if 0 (;@2;)
        i32.const 0
        set_local 21
        get_local 6
        get_local 21
        i32.store offset=28
        br 1 (;@1;)
      end
      get_local 6
      i32.load8_u offset=11
      set_local 22
      i32.const 1
      set_local 23
      get_local 22
      get_local 23
      i32.and
      set_local 24
      get_local 6
      get_local 24
      i32.store offset=28
    end
    get_local 6
    i32.load offset=28
    set_local 25
    i32.const 32
    set_local 26
    get_local 6
    get_local 26
    i32.add
    set_local 27
    get_local 27
    set_global 0
    get_local 25
    return)
  (func (;11;) (type 4) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    get_global 0
    set_local 3
    i32.const 32
    set_local 4
    get_local 3
    get_local 4
    i32.sub
    set_local 5
    get_local 5
    set_global 0
    i32.const 0
    set_local 6
    get_local 5
    get_local 0
    i32.store offset=28
    get_local 5
    get_local 1
    i32.store offset=24
    get_local 5
    get_local 2
    i32.store offset=20
    get_local 5
    get_local 6
    i32.store offset=16
    get_local 5
    get_local 6
    i32.store offset=12
    block  ;; label = @1
      loop  ;; label = @2
        get_local 5
        i32.load offset=12
        set_local 7
        get_local 5
        i32.load offset=20
        set_local 8
        get_local 7
        set_local 9
        get_local 8
        set_local 10
        get_local 9
        get_local 10
        i32.lt_s
        set_local 11
        get_local 11
        set_local 12
        get_local 12
        i32.eqz
        br_if 1 (;@1;)
        i32.const 0
        set_local 13
        get_local 5
        get_local 13
        i32.store offset=8
        block  ;; label = @3
          loop  ;; label = @4
            get_local 5
            i32.load offset=8
            set_local 14
            get_local 5
            i32.load offset=24
            set_local 15
            get_local 5
            i32.load offset=12
            set_local 16
            i32.const 3
            set_local 17
            get_local 16
            get_local 17
            i32.shl
            set_local 18
            get_local 15
            get_local 18
            i32.add
            set_local 19
            get_local 19
            i32.load offset=4
            set_local 20
            get_local 14
            set_local 21
            get_local 20
            set_local 22
            get_local 21
            get_local 22
            i32.lt_u
            set_local 23
            get_local 23
            set_local 24
            get_local 24
            i32.eqz
            br_if 1 (;@3;)
            get_local 5
            i32.load offset=24
            set_local 25
            get_local 5
            i32.load offset=12
            set_local 26
            i32.const 3
            set_local 27
            get_local 26
            get_local 27
            i32.shl
            set_local 28
            get_local 25
            get_local 28
            i32.add
            set_local 29
            get_local 29
            i32.load
            set_local 30
            get_local 5
            i32.load offset=8
            set_local 31
            get_local 30
            get_local 31
            i32.add
            set_local 32
            get_local 32
            i32.load8_u
            set_local 33
            i32.const 24
            set_local 34
            get_local 33
            get_local 34
            i32.shl
            set_local 35
            get_local 35
            get_local 34
            i32.shr_u
            set_local 36
            get_local 36
            call 0
            get_local 5
            i32.load offset=8
            set_local 37
            i32.const 1
            set_local 38
            get_local 37
            get_local 38
            i32.add
            set_local 39
            get_local 5
            get_local 39
            i32.store offset=8
            br 0 (;@4;)
          end
        end
        get_local 5
        i32.load offset=24
        set_local 40
        get_local 5
        i32.load offset=12
        set_local 41
        i32.const 3
        set_local 42
        get_local 41
        get_local 42
        i32.shl
        set_local 43
        get_local 40
        get_local 43
        i32.add
        set_local 44
        get_local 44
        i32.load offset=4
        set_local 45
        get_local 5
        i32.load offset=16
        set_local 46
        get_local 46
        get_local 45
        i32.add
        set_local 47
        get_local 5
        get_local 47
        i32.store offset=16
        get_local 5
        i32.load offset=12
        set_local 48
        i32.const 1
        set_local 49
        get_local 48
        get_local 49
        i32.add
        set_local 50
        get_local 5
        get_local 50
        i32.store offset=12
        br 0 (;@2;)
      end
    end
    get_local 5
    i32.load offset=16
    set_local 51
    i32.const 32
    set_local 52
    get_local 5
    get_local 52
    i32.add
    set_local 53
    get_local 53
    set_global 0
    get_local 51
    return)
  (table (;0;) 8 8 anyfunc)
  (memory (;0;) 2)
  (global (;0;) (mut i32) (i32.const 66592))
  (global (;1;) i32 (i32.const 66592))
  (global (;2;) i32 (i32.const 1052))
  (export "memory" (memory 0))
  (export "__heap_base" (global 1))
  (export "__data_end" (global 2))
  (export "Match" (func 10))
  (export "writev_c" (func 11))
  (elem (i32.const 1) 2 3 4 5 6 7 8)
  (data (i32.const 1024) "\01\00\00\00\02\00\00\00\03\00\00\00\04\00\00\00\05\00\00\00\06\00\00\00\07\00\00\00"))
