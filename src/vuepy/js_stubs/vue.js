/**
 * stub for vue.js
 */

export function reactive(obj) {
  return new Proxy(obj, {
    get(target, key) {
      track(target, key)
      return target[key]
    },
    set(target, key, value) {
      target[key] = value
      trigger(target, key)
    }
  })
}

export function ref(value) {
  const refObject = {
    get value() {
      track(refObject, 'value')
      return value
    },
    set value(newValue) {
      value = newValue
      trigger(refObject, 'value')
    }
  }
  return refObject
}


export function watch(source, callback, options) {
  // return StopHandle;
}

export function computed(getter, debuggerOptions) {
  // return Readonly<Ref<Readonly<T>>>
}

export function computed(options, debuggerOptions) {
  // return Ref<T>
}
