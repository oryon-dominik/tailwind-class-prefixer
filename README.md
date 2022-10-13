# auto prefix tailwind classes

prefix handle default: "tw-"

## media Queries:

    foobar:sm
    ->
    foobar:tw-sm

## vue class bindings:

    <div :class="{ active: isActive }"></div>
    -> 
    <div :class="{ tw-active: isActive }"></div>

## tw class list

    get from whereever


    add tw- also to apply classes in .css files


## check or add the config

    `tailwind.config.js`

    module.exports = {
    prefix: 'tw-',
    }


## regexes for matching

    https://pythex.org/
